# shipment_optimizer/optimizer.py

class ShipmentOptimizer:
    """
    A class to optimize shipment assignments to drivers and vehicles.
    """

    def __init__(self, shipments, drivers, vehicles):
        """
        Initialize the optimizer with available shipments, drivers, and vehicles.
        :param shipments: List of shipments
        :param drivers: List of drivers
        :param vehicles: List of vehicles
        """
        self.shipments = shipments
        self.drivers = drivers
        self.vehicles = vehicles

    def prioritize_shipments(self):
        """
        Prioritize shipments based on deadlines and priority levels.
        Sorts shipments in place by delivery deadline.
        """
        self.shipments.sort(key=lambda x: x.get('deadline'))

    def assign(self):
        """
        Assign shipments to available drivers and vehicles.
        Returns a dictionary of assignments.
        """
        assignments = []
        for shipment in self.shipments:
            if not self.drivers or not self.vehicles:
                break  # Stop if no drivers or vehicles available

            driver = self.drivers.pop(0)  # Get the next available driver
            vehicle = self.vehicles.pop(0)  # Get the next available vehicle

            assignments.append({
                'shipment_id': shipment.get('id'),
                'driver': driver.get('name'),
                'vehicle': vehicle.get('id'),
            })

        return assignments
