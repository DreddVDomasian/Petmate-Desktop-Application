import json, os
from PyQt6.QtWidgets import QCompleter
from PyQt6.QtCore import Qt
from input_styles import completer_popup_style

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

    def set_dynamic_completer(self, comboBox):
        """Attach completer that always matches current combobox items"""
        completer = QCompleter(comboBox.model())
        completer.setCompletionColumn(0)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
        completer.popup().setStyleSheet(completer_popup_style)
        comboBox.setCompleter(completer)

    def load_provinces(self):
        self.provinceComboBox.clear()
        self.provinceComboBox.addItem("", None)
        for prov in sorted(self.provinces, key=lambda x: x["name"]):
            self.provinceComboBox.addItem(prov["name"], prov["prov_code"])

        # set completer based on current items
        self.set_dynamic_completer(self.provinceComboBox)

    def on_province_selected(self, index):
        self.cityComboBox.clear()
        self.cityComboBox.addItem("", None)
        self.barangayComboBox.clear()
        self.barangayComboBox.addItem("", None)

        if index == 0:
            return

        prov_code = self.provinceComboBox.itemData(index)
        filtered = sorted(
            [c for c in self.cities if c["prov_code"] == prov_code],
            key=lambda x: x["name"]
        )
        for city in filtered:
            self.cityComboBox.addItem(city["name"], city["mun_code"])

        # update completer for cities
        self.set_dynamic_completer(self.cityComboBox)

    def on_city_selected(self, index):
        self.barangayComboBox.clear()
        self.barangayComboBox.addItem("", None)

        if index == 0:
            return

        mun_code = self.cityComboBox.itemData(index)
        filtered = sorted(
            [b for b in self.barangays if b["mun_code"] == mun_code],
            key=lambda x: x["name"]
        )
        for brgy in filtered:
            self.barangayComboBox.addItem(brgy["name"])

        # update completer for barangays
        self.set_dynamic_completer(self.barangayComboBox)
