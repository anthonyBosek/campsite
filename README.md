# REST-ful Campsite Practice

### Campsite API
Build out a full RESTful Flask API for park AND campsite resources with models, migration(s), routes, resource classes and view methods.  Models should have the following properties:
```python
park = {
    "name": str,
    "address": str,
    "entrance_fee": float,
    "has_trails": bool,
    "has_RV_cleanout": bool,
    "begin_camping_season": date,
    "end_camping_season": date
}
campsite = {
    "park_id": int,
    "max_capcity": int,
    "type": str,
    "site_fee": float,
    "has_water": bool,
    "has_bathroom": bool,
    "has_grill": bool
}
```
Your models should also have the following constraints or validations:
- Park
  - name must be unique
  - address must be present
  - entrance fee is between $13.99 - $25.00
- Campsite
  - max capacity is less than or equal to 10
  - type is either "tent" or "RV"


You don't need all 5 RESTful routes for both resources, but between the two resources, all 5 types of routes should be used.

### BONUS
- Add another model for reservations. Reservations must belong to a campsite and have a start and end date. Dates must fall within camping season for the park.
- Add error handling to your routes.
