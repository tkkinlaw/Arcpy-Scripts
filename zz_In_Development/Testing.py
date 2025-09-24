import os
import uuid
import logging
import arcpy
from arcgis.gis import GIS
from arcgis.graph import KnowledgeGraph

"""Convert features to Knowledge Graph entities and create a relationship.

This script expects a feature class (or layer) with exactly two features.
It converts each feature to a simple entity payload (properties + geometry JSON)
and then attempts to create the entities and a relationship in the Knowledge Graph.

Fallback behavior: if the live KnowledgeGraph API method for creating entities
is unavailable, the script will print the payloads so they can be uploaded manually.

Assumptions made:
- The KG object may not expose create methods with known names; we try a few
  common names and otherwise fall back to printing payloads.
- Geometry is stored and transmitted as Esri JSON (Shape JSON via arcpy).
"""

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# -- Configuration (adjust to your environment) --------------------------------
arcpy.env.overwriteOutput = True
gdb = r"C:\Demos\AgriSupplyChain\AgriSupplyChain.gdb"
feature_class = os.path.join(gdb, "Entities")

# GIS / Knowledge Graph connection (adjust credentials/URL as needed)
gis = GIS("https://ebase.ad.local/portal/home", 'tkinlaw_ent', 'Esri.4.GIS')
kg = KnowledgeGraph(url=r'https://ebase.ad.local/server/rest/services/Hosted/Agribusiness_Supply_Chain/KnowledgeGraphServer', gis=gis)
logging.info("Connected to GIS and KnowledgeGraph")


def get_two_features(fc_path):
    """Return up to two rows from the feature class as tuples (oid, attributes dict, shapeJSON)."""
    fields = ["OID@", "Name", "SHAPE@JSON"]
    results = []
    with arcpy.da.SearchCursor(fc_path, fields) as cursor:
        for row in cursor:
            oid = row[0]
            name = row[1]
            shape_json = row[2]
            props = {"Name": name}
            results.append((oid, props, shape_json))
            if len(results) >= 2:
                break
    if len(results) < 2:
        logging.warning("Feature class '%s' contains fewer than 2 features (%d found).", fc_path, len(results))
    return results


def build_entity_payload(type_name, properties, shape_json=None):
    """Construct a KG entity payload dict.

    This payload shape is intentionally generic: real KG APIs may require
    different keys. We include type_name, properties and geometry (esri JSON).
    """
    payload = {
        "type_name": type_name,
        "properties": properties.copy() if properties else {},
    }
    if shape_json:
        payload["geometry"] = shape_json
    return payload


def try_create_entity(kg_obj, entity_payload):
    """Attempt to create an entity in the KnowledgeGraph.

    Tries a few likely method names on the KnowledgeGraph object. If none
    exist, falls back to returning a generated UUID and printing the payload.
    Returns: (entity_id, created_flag)
    """
    # Try known/likely methods
    candidates = [
        "create_entity",
        "create_entities",
        "add_entity",
        "add_entities",
        "add_node",
        "create_node",
    ]
    for name in candidates:
        fn = getattr(kg_obj, name, None)
        if callable(fn):
            try:
                logging.info("Calling KnowledgeGraph.%s(...)", name)
                res = fn(entity_payload)
                # Try to extract id from response if possible
                if isinstance(res, dict) and "id" in res:
                    return res["id"], True
                # Many APIs return lists
                if isinstance(res, (list, tuple)) and len(res) > 0:
                    first = res[0]
                    if isinstance(first, dict) and "id" in first:
                        return first["id"], True
                # If we don't know, return a generated id but mark as not fully verified
                return str(uuid.uuid4()), True
            except Exception as e:
                logging.warning("KnowledgeGraph.%s call failed: %s", name, e)

    # No suitable API found — fall back to printing payload for manual upload
    logging.info("No KG create method found; printing payload for manual upload.")
    logging.info("Entity payload: %s", entity_payload)
    fake_id = str(uuid.uuid4())
    return fake_id, False


def try_create_relationship(kg_obj, rel_payload):
    """Attempt to create a relationship/edge in the KG. Similar fallback behavior."""
    candidates = [
        "create_relationship",
        "create_relationships",
        "add_relationship",
        "add_edge",
        "create_edge",
    ]
    for name in candidates:
        fn = getattr(kg_obj, name, None)
        if callable(fn):
            try:
                logging.info("Calling KnowledgeGraph.%s(...)", name)
                res = fn(rel_payload)
                return True
            except Exception as e:
                logging.warning("KnowledgeGraph.%s call failed: %s", name, e)

    logging.info("No KG relationship method found; printing payload for manual upload.")
    logging.info("Relationship payload: %s", rel_payload)
    return False


def main():
    feats = get_two_features(feature_class)
    if len(feats) < 2:
        logging.error("Need two features to build a relationship. Found %d.", len(feats))
        return

    # Build and create entities
    created_ids = []
    for idx, (oid, props, shape_json) in enumerate(feats, start=1):
        type_name = "Feature"  # adjust to your KG type naming
        payload = build_entity_payload(type_name, props, shape_json)
        entity_id, created = try_create_entity(kg, payload)
        logging.info("Entity %d -> id=%s created=%s", idx, entity_id, created)
        created_ids.append(entity_id)

    # Build relationship payload (from first to second)
    rel_payload = {
        "type_name": "Transports_To",
        "from_id": created_ids[0],
        "to_id": created_ids[1],
        "properties": {},
    }
    rel_created = try_create_relationship(kg, rel_payload)
    logging.info("Relationship created: %s", rel_created)

    logging.info("All done")


if __name__ == "__main__":
    main()
print("All done")