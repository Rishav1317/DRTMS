# ============================================================
# DRTMS Core Logic — Disaster Relief Resource Management System
# ============================================================
from datetime import datetime


class Resource:
    def __init__(self, resource_id, name, resource_type, quantity, unit):
        self.resource_id = resource_id
        self.name = name
        self.resource_type = resource_type
        self.quantity = quantity
        self.available_quantity = quantity
        self.unit = unit
        self.allocated_to = {}

    def to_dict(self):
        return {
            "resource_id": self.resource_id,
            "name": self.name,
            "resource_type": self.resource_type,
            "quantity": self.quantity,
            "available_quantity": self.available_quantity,
            "unit": self.unit,
            "allocated_to": self.allocated_to,
        }


class DisasterEvent:
    def __init__(self, disaster_id, name, location, severity, disaster_type):
        self.disaster_id = disaster_id
        self.name = name
        self.location = location
        self.severity = severity
        self.disaster_type = disaster_type
        self.status = "Active"
        self.registered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.allocated_resources = {}

    def to_dict(self):
        return {
            "disaster_id": self.disaster_id,
            "name": self.name,
            "location": self.location,
            "severity": self.severity,
            "disaster_type": self.disaster_type,
            "status": self.status,
            "registered_at": self.registered_at,
            "allocated_resources": self.allocated_resources,
        }


class DRTMS:
    def __init__(self):
        self.resources = {}
        self.disasters = {}
        self.allocation_log = []
        self._load_initial_inventory()

    def _load_initial_inventory(self):
        data = [
            ("R001", "Food Packets",           "Food",       1000, "packets"),
            ("R002", "Water Bottles",          "Water",       500, "litres"),
            ("R003", "Medical First-Aid Kits", "Medical",     200, "kits"),
            ("R004", "Rescue Personnel",       "Personnel",    50, "persons"),
            ("R005", "Emergency Tents",        "Shelter",     100, "units"),
            ("R006", "Blankets",               "Shelter",     300, "pieces"),
            ("R007", "Generator Sets",         "Equipment",    20, "units"),
        ]
        for args in data:
            self.add_resource(*args)

    # ── Resource ────────────────────────────────────────────
    def add_resource(self, resource_id, name, resource_type, quantity, unit):
        if resource_id in self.resources:
            return False, f"Resource ID '{resource_id}' already exists."
        if quantity <= 0:
            return False, "Quantity must be greater than 0."
        self.resources[resource_id] = Resource(resource_id, name, resource_type, quantity, unit)
        return True, f"Resource '{name}' added successfully."

    # ── Disaster ─────────────────────────────────────────────
    def register_disaster(self, disaster_id, name, location, severity, disaster_type):
        if not disaster_id or not name or not location:
            return False, "Disaster ID, name, and location are mandatory."
        if disaster_id in self.disasters:
            return False, f"Disaster ID '{disaster_id}' already exists."
        if not isinstance(severity, int) or not (1 <= severity <= 5):
            return False, "Severity must be an integer between 1 and 5."
        self.disasters[disaster_id] = DisasterEvent(disaster_id, name, location, severity, disaster_type)
        return True, f"Disaster '{name}' registered at {location} (Severity: {severity}/5)."

    # ── Allocate ─────────────────────────────────────────────
    def allocate_resource(self, disaster_id, resource_id, quantity):
        if disaster_id not in self.disasters:
            return False, f"Disaster ID '{disaster_id}' not found in the system."
        if resource_id not in self.resources:
            return False, f"Resource ID '{resource_id}' not found in inventory."
        if not isinstance(quantity, int) or quantity <= 0:
            return False, "Quantity must be a positive integer."
        disaster = self.disasters[disaster_id]
        resource = self.resources[resource_id]
        if disaster.status != "Active":
            return False, f"Disaster '{disaster_id}' is not active (status: {disaster.status})."
        if resource.available_quantity < quantity:
            return False, f"Insufficient stock. Requested: {quantity}, Available: {resource.available_quantity} {resource.unit}."
        resource.available_quantity -= quantity
        resource.allocated_to[disaster_id] = resource.allocated_to.get(disaster_id, 0) + quantity
        disaster.allocated_resources[resource_id] = disaster.allocated_resources.get(resource_id, 0) + quantity
        self.allocation_log.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": "ALLOCATE",
            "disaster_id": disaster_id,
            "disaster_name": disaster.name,
            "resource_id": resource_id,
            "resource_name": resource.name,
            "quantity": quantity,
            "unit": resource.unit,
        })
        return True, f"Allocated {quantity} {resource.unit} of '{resource.name}' to '{disaster.name}'."

    # ── Release ──────────────────────────────────────────────
    def release_resource(self, disaster_id, resource_id, quantity):
        if disaster_id not in self.disasters:
            return False, f"Disaster ID '{disaster_id}' not found."
        if resource_id not in self.resources:
            return False, f"Resource ID '{resource_id}' not found."
        if not isinstance(quantity, int) or quantity <= 0:
            return False, "Quantity must be a positive integer."
        disaster = self.disasters[disaster_id]
        resource = self.resources[resource_id]
        if resource_id not in disaster.allocated_resources:
            return False, f"Resource '{resource_id}' is not allocated to disaster '{disaster_id}'."
        if disaster.allocated_resources[resource_id] < quantity:
            return False, f"Cannot release {quantity}. Only {disaster.allocated_resources[resource_id]} {resource.unit} allocated."
        disaster.allocated_resources[resource_id] -= quantity
        resource.available_quantity += quantity
        if disaster.allocated_resources[resource_id] == 0:
            del disaster.allocated_resources[resource_id]
        self.allocation_log.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": "RELEASE",
            "disaster_id": disaster_id,
            "disaster_name": disaster.name,
            "resource_id": resource_id,
            "resource_name": resource.name,
            "quantity": quantity,
            "unit": resource.unit,
        })
        return True, f"Released {quantity} {resource.unit} of '{resource.name}' from '{disaster.name}'."

    # ── Stats ─────────────────────────────────────────────────
    def get_stats(self):
        total_resources = len(self.resources)
        total_disasters = len(self.disasters)
        active_disasters = sum(1 for d in self.disasters.values() if d.status == "Active")
        total_allocations = len([l for l in self.allocation_log if l["action"] == "ALLOCATE"])
        return {
            "total_resources": total_resources,
            "total_disasters": total_disasters,
            "active_disasters": active_disasters,
            "total_allocations": total_allocations,
            "total_log_entries": len(self.allocation_log),
        }

    # ── Test Cases ────────────────────────────────────────────
    def run_test_cases(self):
        system = DRTMS()
        results = []

        def check(tc_id, label, category, result, expected_pass):
            status = "PASS" if result == expected_pass else "FAIL"
            results.append({"id": tc_id, "label": label, "category": category, "status": status})

        # Valid
        r, _ = system.register_disaster("D001", "Chennai Cyclone 2026", "Chennai, Tamil Nadu", 4, "Cyclone")
        check("TC-V01", "Register valid disaster event", "valid", r, True)
        r, _ = system.register_disaster("D002", "Kerala Flood 2026", "Kochi, Kerala", 5, "Flood")
        check("TC-V02", "Register second valid disaster", "valid", r, True)
        r, _ = system.allocate_resource("D001", "R001", 200)
        check("TC-V03", "Allocate food packets to D001", "valid", r, True)
        r, _ = system.allocate_resource("D001", "R002", 100)
        check("TC-V04", "Allocate water bottles to D001", "valid", r, True)
        r, _ = system.allocate_resource("D002", "R003", 50)
        check("TC-V05", "Allocate medical kits to D002", "valid", r, True)
        r, _ = system.allocate_resource("D001", "R004", 15)
        check("TC-V06", "Allocate rescue personnel to D001", "valid", r, True)
        r, _ = system.release_resource("D001", "R001", 50)
        check("TC-V07", "Release 50 food packets from D001", "valid", r, True)
        avail = system.resources["R005"].available_quantity
        r, _ = system.allocate_resource("D002", "R005", avail)
        check("TC-V08", "Allocate all available tents to D002", "valid", r, True)

        # Invalid
        r, _ = system.register_disaster("D001", "Duplicate", "Unknown", 3, "Flood")
        check("TC-I01", "Duplicate disaster ID (should fail)", "invalid", r, False)
        r, _ = system.register_disaster("D003", "Test", "Mumbai", 7, "Flood")
        check("TC-I02", "Severity=7 out of range (should fail)", "invalid", r, False)
        r, _ = system.allocate_resource("D999", "R001", 50)
        check("TC-I03", "Non-existent disaster ID (should fail)", "invalid", r, False)
        r, _ = system.allocate_resource("D001", "R999", 50)
        check("TC-I04", "Non-existent resource ID (should fail)", "invalid", r, False)
        r, _ = system.allocate_resource("D001", "R003", 99999)
        check("TC-I05", "Exceed available stock (should fail)", "invalid", r, False)
        r, _ = system.allocate_resource("D001", "R002", 0)
        check("TC-I06", "Zero quantity (should fail)", "invalid", r, False)
        r, _ = system.allocate_resource("D001", "R002", -10)
        check("TC-I07", "Negative quantity (should fail)", "invalid", r, False)
        r, _ = system.release_resource("D001", "R001", 99999)
        check("TC-I08", "Release more than allocated (should fail)", "invalid", r, False)
        r, _ = system.release_resource("D002", "R001", 10)
        check("TC-I09", "Release not-allocated resource (should fail)", "invalid", r, False)
        r, _ = system.register_disaster("", "Empty ID", "Location", 3, "Flood")
        check("TC-I10", "Empty disaster ID (should fail)", "invalid", r, False)

        passed = sum(1 for r in results if r["status"] == "PASS")
        return {
            "results": results,
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
        }
