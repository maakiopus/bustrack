#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from NovaApi.ExecuteAction.LocateTracker.location_request import get_location_data_for_device

if __name__ == '__main__':
    print(get_location_data_for_device("68a847d6-0000-268b-a6f6-34c7e9210863","GoogleFindMyTools µC"))
