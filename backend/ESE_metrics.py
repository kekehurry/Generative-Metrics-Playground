import pandas as pd

# Economic nested classes

class Employment:
    def __init__(self, data):
        self.unemployment_rate = data['unemployment_rate']
        self.local_job_creation = data['local_job_creation']

class Equity:
    def __init__(self, data):
        self.affordability_of_housing = data['affordability_of_housing']
        self.cost_of_housing = data['cost_of_housing']

class Income:
    def __init__(self, data):
        self.median_disposable_income = data['median_disposable_income']

class Innovation:
    def __init__(self, data):
        self.creative_industry = data['creative_industry']
        self.research_intensity = data['research_intensity']

class AttractivenessCompetitiveness:
    def __init__(self, data):
        self.congestion = data['congestion']
        self.public_transport_use = data['public_transport_use']
        self.population_dependency_ratio = data['population_dependency_ratio']
        self.tourism_intensity = data['tourism_intensity']
        self.visitor_access = data['visitor_access']
        self.decreased_travel_time = data['decreased_travel_time']

class BuildUpArea:
    def __init__(self, data):
        self.new_developed_build_up_area = data['new_developed_build_up_area']

class Displacement:
    def __init__(self, data):
        self.business_displace_competition = data['business_displace_competition']
        self.residents_displacement = data['residents_displacement']
        self.service_population_supporting = data['service_population_supporting']

class Economic:
    def __init__(self, file_path):
        data = pd.read_csv(file_path)
        self.employment = Employment(data)
        self.equity = Equity(data)
        self.income = Income(data)
        self.innovation = Innovation(data)
        self.attractiveness_competitiveness = AttractivenessCompetitiveness(data)
        self.build_up_area = BuildUpArea(data)
        self.displacement = Displacement(data)
        self._preprocess(data)

    def _preprocess(self, data):
        data.fillna(0, inplace=True)

    def get_statistics(self):
        return self.data.describe()

# Environmental nested classes

class Pollution:
    def __init__(self, data):
        self.air_quality = data['air_quality']
        self.noise_pollution = data['noise_pollution']

class Ecosystem:
    def __init__(self, data):
        self.share_of_green_and_water_space = data['share_of_green_and_water_space']

class PublicService:
    def __init__(self, data):
        self.quantity_of_public_green_space = data['quantity_of_public_green_space']
        self.delivery_and_proximity_to_amenities = data['delivery_and_proximity_to_amenities']

class Energy:
    def __init__(self, data):
        self.co2_emissions_mobility = data['co2_emissions_mobility']
        self.co2_emissions_building = data['co2_emissions_building']

class Land:
    def __init__(self, data):
        self.brownfield_use = data['brownfield_use']
        self.urban_heat_island = data['urban_heat_island']

class Environmental:
    def __init__(self, file_path):
        data = pd.read_csv(file_path)
        self.pollution = Pollution(data)
        self.ecosystem = Ecosystem(data)
        self.public_service = PublicService(data)
        self.energy = Energy(data)
        self.land = Land(data)
        self._preprocess(data)

    def _preprocess(self, data):
        data.fillna(0, inplace=True)

    def get_statistics(self):
        return self.data.describe()

# Social nested classes

class SafetySecurity:
    def __init__(self, data):
        self.traffic_accidents = data['traffic_accidents']
        self.crime_rate = data['crime_rate']

class AccessToService:
    def __init__(self, data):
        self.access_to_public_transport = data['access_to_public_transport']
        self.access_to_vehicle_sharing_solutions_for_city_travel = data['access_to_vehicle_sharing_solutions_for_city_travel']
        self.access_to_public_amenities = data['access_to_public_amenities']
        self.access_to_commercial_amenities = data['access_to_commercial_amenities']

class Education:
    def __init__(self, data):
        self.access_to_educational_resources = data['access_to_educational_resources']

class Housing:
    def __init__(self, data):
        self.diversity_of_housing = data['diversity_of_housing']
        self.preservation_of_cultural_heritage = data['preservation_of_cultural_heritage']
        self.ground_floor_usage = data['ground_floor_usage']
        self.public_outdoor_recreation_space = data['public_outdoor_recreation_space']
        self.green_space = data['green_space']

class SocialExposureDensity:
    def __init__(self, data):
        self.population_density = data['population_density']

class JobHousing:
    def __init__(self, data):
        self.job_housing_ratio = data['job_housing_ratio']

class Social:
    def __init__(self, file_path):
        data = pd.read_csv(file_path)
        self.safety_security = SafetySecurity(data)
        self.access_to_service = AccessToService(data)
        self.education = Education(data)
        self.housing = Housing(data)
        self.social_exposure_density = SocialExposureDensity(data)
        self.job_housing = JobHousing(data)
        self._preprocess(data)

    def _preprocess(self, data):
        data.fillna(0, inplace=True)

    def get_statistics(self):
        return self.data.describe()

#--------------------------------------------#
# Test
#--------------------------------------------#

def test():
    economic = Economic("economic.csv")
    print(economic.employment.unemployment_rate)
    print(economic.get_statistics())

    environmental = Environmental("environmental.csv")
    print(environmental.pollution.air_quality)
    print(environmental.get_statistics())

    social = Social("social.csv")
    print(social.safety_security.traffic_accidents)
    print(social.get_statistics())

if __name__ == '__main__':
    test()
