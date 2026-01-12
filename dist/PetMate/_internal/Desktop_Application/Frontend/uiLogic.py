import json, os
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QCompleter, QComboBox
from Desktop_Application.Frontend.input_styles import completer_popup_style


class AddressDataLoader(QThread):
    loaded = pyqtSignal(object)  # {'provinces': [...], 'cities': [...], 'barangays': [...]}
    error = pyqtSignal(str)

    def __init__(self, base_dir: str):
        super().__init__()
        self.base_dir = base_dir

    def run(self):
        try:
            with open(os.path.join(self.base_dir, "AddressJSON", "provinces.json"), "r", encoding="utf-8") as f:
                provinces = json.load(f)
            with open(os.path.join(self.base_dir, "AddressJSON", "cities.json"), "r", encoding="utf-8") as f:
                cities = json.load(f)
            with open(os.path.join(self.base_dir, "AddressJSON", "barangays.json"), "r", encoding="utf-8") as f:
                barangays = json.load(f)
            self.loaded.emit({"provinces": provinces, "cities": cities, "barangays": barangays})
        except Exception as e:
            self.error.emit(str(e))

class UIHandler:
    def __init__(self, provinceComboBox, cityComboBox, barangayComboBox):
        self.provinceComboBox = provinceComboBox
        self.cityComboBox = cityComboBox
        self.barangayComboBox = barangayComboBox

        self._base_dir = os.path.dirname(__file__)
        self._loader = None

        # Loaded asynchronously to avoid blocking app startup.
        self.provinces = None
        self.cities = None
        self.barangays = None

        self.provinceComboBox.currentIndexChanged.connect(self.on_province_selected)
        self.cityComboBox.currentIndexChanged.connect(self.on_city_selected)

    def is_loaded(self) -> bool:
        return self.provinces is not None and self.cities is not None and self.barangays is not None

    def load_address_data_async(self, on_ready=None, on_error=None):
        """Load AddressJSON in the background.

        on_ready: called (no args) after provinces/cities/barangays are available.
        on_error: called with error message (str).
        """
        if self.is_loaded():
            if on_ready:
                on_ready()
            return

        # Avoid starting multiple loaders
        if self._loader is not None and self._loader.isRunning():
            return

        self._loader = AddressDataLoader(self._base_dir)

        def _loaded(payload):
            try:
                if isinstance(payload, dict):
                    self.provinces = payload.get('provinces')
                    self.cities = payload.get('cities')
                    self.barangays = payload.get('barangays')
                if on_ready:
                    on_ready()
            finally:
                self._loader = None

        def _error(msg):
            try:
                if on_error:
                    on_error(msg)
            finally:
                self._loader = None

        self._loader.loaded.connect(_loaded)
        self._loader.error.connect(_error)
        self._loader.start()


    def set_dynamic_completer(self, comboBox):
        """Attach completer that always matches current combobox items"""
        completer = QCompleter(comboBox.model())
        completer.setCompletionColumn(0)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
        completer.popup().setStyleSheet(completer_popup_style)
        comboBox.setCompleter(completer)

    def load_provinces(self):
        if not self.is_loaded():
            # Data not yet loaded; caller should call load_address_data_async first.
            return
        self.provinceComboBox.clear()
        self.provinceComboBox.addItem("", None)
        for prov in sorted(self.provinces, key=lambda x: x["name"]):
            self.provinceComboBox.addItem(prov["name"].title(), prov["prov_code"])

        # set completer based on current items
        self.set_dynamic_completer(self.provinceComboBox)

    def on_province_selected(self, index):
        if not self.is_loaded():
            return
        self.cityComboBox.clear()
        self.cityComboBox.addItem("", None)
        self.barangayComboBox.clear()
        self.barangayComboBox.addItem("", None)

        if index == 0:
            self.cityComboBox.setEnabled(False)
            self.barangayComboBox.setEnabled(False)
            return

        prov_code = self.provinceComboBox.itemData(index)
        filtered = sorted(
            [c for c in self.cities if c["prov_code"] == prov_code],
            key=lambda x: x["name"]
        )
        for city in filtered:
            self.cityComboBox.addItem(city["name"].title(), city["mun_code"])

        # update completer for cities
        self.set_dynamic_completer(self.cityComboBox)

        self.cityComboBox.setEnabled(True)

    def on_city_selected(self, index):
        if not self.is_loaded():
            return
        self.barangayComboBox.clear()
        self.barangayComboBox.addItem("", None)

        if index == 0:
            self.barangayComboBox.setEnabled(False)
            return

        mun_code = self.cityComboBox.itemData(index)
        filtered = sorted(
            [b for b in self.barangays if b["mun_code"] == mun_code],
            key=lambda x: x["name"]
        )
        for brgy in filtered:
            self.barangayComboBox.addItem(brgy["name"].title())

        # update completer for barangays
        self.set_dynamic_completer(self.barangayComboBox)
        self.barangayComboBox.setEnabled(True)

