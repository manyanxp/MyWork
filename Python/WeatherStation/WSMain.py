from Weather.WeatherStation import Weatherstation, WeatherInfomation, WeatherInfomationKind
from Weather.DataModel import AtmosphericInformation
from datetime import date

def main():
    station = Weatherstation('localhost', 27017, 'weatherstation', 'AtmosphericInformation')
    station.Test()
    atom = AtmosphericInformation()
    atom.Temperature = 1.0
    info = WeatherInfomation(date.today(), WeatherInfomationKind.Normal.value, atom)
    info.atom.Temperature = 1.0
    station.Insert(info)
    station.Select(date.today(), date.today())

if __name__ == '__main__':
    main()
