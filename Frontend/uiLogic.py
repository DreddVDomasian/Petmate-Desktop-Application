import json, os
from PyQt6.QtWidgets import QComboBox

class UIHandler:
    def __init__(self, provinceComboBox, cityComboBox, barangayComboBox):
        self.provinceComboBox = provinceComboBox
        self.cityComboBox = cityComboBox
        self.barangayComboBox = barangayComboBox


        base_dir = os.path.dirname(__file__)
        with open(os.path.join(base_dir, "AddressJSON", "provinces.json"), "r", encoding="utf-8") as f:
            self.provinces = json.load(f)
        with open(os.path.join(base_dir, "AddressJSON", "cities.json"), "r", encoding="utf-8") as f:
            self.cities = json.load(f)
        with open(os.path.join(base_dir, "AddressJSON", "barangays.json"), "r", encoding="utf-8") as f:
            self.barangays = json.load(f)

        self.provinceComboBox.currentIndexChanged.connect(self.on_province_selected)
        self.cityComboBox.currentIndexChanged.connect(self.on_city_selected)

    def load_provinces(self):
        self.provinceComboBox.clear()
        self.provinceComboBox.addItem("Select Province")
        for prov in sorted(self.provinces, key=lambda x: x["name"]):
            self.provinceComboBox.addItem(prov["name"], prov["prov_code"])

    def on_province_selected(self, index):
        self.cityComboBox.clear()
        self.barangayComboBox.clear()
        if index == 0:
            return
        prov_code = self.provinceComboBox.itemData(index)
        filtered = sorted([c for c in self.cities if c["prov_code"] == prov_code], key=lambda x: x["name"])
        self.cityComboBox.addItem("Select City/Municipality")
        for city in filtered:
            self.cityComboBox.addItem(city["name"], city["mun_code"])

    def on_city_selected(self, index):
        self.barangayComboBox.clear()
        if index == 0:
            return
        mun_code = self.cityComboBox.itemData(index)
        filtered = sorted([b for b in self.barangays if b["mun_code"] == mun_code], key=lambda x: x["name"])
        self.barangayComboBox.addItem("Select Barangay")
        for brgy in filtered:
            self.barangayComboBox.addItem(brgy["name"])

