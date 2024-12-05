
# Auto-generated python file from make_elements.py
from dataclasses import dataclass

@dataclass()
class ElementData():
    atomic_number: int
    symbol: str
    name: str
    MAI_mass: int
    MAI_weight: float
    natural_weight: float
    density: float
    atomic_density: float
    fermi_velocity: float
    heat_subl: float
    gasdens: float
    gas_density: float

ELEM_DICT = {
"H": ElementData(1, "H", "Hydrogen", 1, 1.008, 1.008, .0715, 4.271E22, 1.031, .00, 8.990E-5, 5.374E19),
"He": ElementData(2, "He", "Helium", 4, 4.003, 4.003, .1259, 1.894E22, .160, .00, 1.787E-4, 2.690E19),
"Li": ElementData(3, "Li", "Lithium", 7, 7.016, 6.941, .5340, 4.633E22, .598, 1.67, .5340, 4.633E22),
"Be": ElementData(4, "Be", "Beryllium", 9, 9.012, 9.012, 1.8480, 1.235E23, 1.078, 3.38, 1.8480, 1.235E23),
"B": ElementData(5, "B", "Boron", 11, 11.009, 10.811, 2.3502, 1.309E23, 1.049, 5.73, 2.3502, 1.309E23),
"C": ElementData(6, "C", "Carbon", 12, 12.000, 12.011, 2.2530, 1.130E23, 1.000, 7.41, 2.2530, 1.130E23),
"N": ElementData(7, "N", "Nitrogen", 14, 14.003, 14.007, 1.0260, 4.411E22, 1.058, .00, 1.251E-3, 5.381E19),
"O": ElementData(8, "O", "Oxygen", 16, 15.995, 15.999, 1.4260, 5.368E22, .939, .00, 1.429E-3, 5.381E19),
"F": ElementData(9, "F", "Fluorine", 19, 18.998, 18.998, 1.1111, 3.522E22, .746, .00, 1.1111, 3.522E22),
"Ne": ElementData(10, "Ne", "Neon", 20, 19.992, 20.180, 1.2040, 3.593E22, .342, .00, 9.010E-4, 2.690E19),
"Na": ElementData(11, "Na", "Sodium", 23, 22.990, 22.990, .9700, 2.541E22, .453, 1.12, .9700, 2.541E22),
"Mg": ElementData(12, "Mg", "Magnesium", 24, 23.985, 24.305, 1.7366, 4.303E22, .711, 1.54, 1.7366, 4.303E22),
"Al": ElementData(13, "Al", "Aluminum", 27, 26.982, 26.982, 2.7020, 6.031E22, .905, 3.36, 2.7020, 6.031E22),
"Si": ElementData(14, "Si", "Silicon", 28, 27.977, 28.086, 2.3212, 4.977E22, .974, 4.70, 2.3212, 4.977E22),
"P": ElementData(15, "P", "Phosphorus", 31, 30.974, 30.974, 1.8219, 3.542E22, .972, 3.27, 1.8219, 3.542E22),
"S": ElementData(16, "S", "Sulfur", 32, 31.972, 32.066, 2.0686, 3.885E22, .899, 2.88, 2.0686, 3.885E22),
"Cl": ElementData(17, "Cl", "Chlorine", 35, 34.969, 35.453, 1.8956, 3.220E22, .708, .00, 1.8956, 3.220E22),
"Ar": ElementData(18, "Ar", "Argon", 40, 39.962, 39.948, 1.6504, 2.488E22, .398, .00, 1.784E-3, 2.691E19),
"K": ElementData(19, "K", "Potassium", 39, 38.964, 39.098, .8632, 1.330E22, .366, .93, .8632, 1.330E22),
"Ca": ElementData(20, "Ca", "Calcium", 40, 39.963, 40.080, 1.5400, 2.314E22, .627, 1.83, 1.5400, 2.314E22),
"Sc": ElementData(21, "Sc", "Scandium", 45, 44.956, 44.956, 2.9890, 4.004E22, .817, 3.49, 2.9890, 4.004E22),
"Ti": ElementData(22, "Ti", "Titanium", 48, 47.950, 47.900, 4.5189, 5.681E22, .994, 4.89, 4.5189, 5.681E22),
"V": ElementData(23, "V", "Vanadium", 51, 50.940, 50.942, 5.9600, 7.046E22, 1.142, 5.33, 5.9600, 7.046E22),
"Cr": ElementData(24, "Cr", "Chromium", 52, 51.940, 51.996, 7.2000, 8.339E22, 1.238, 4.12, 7.2000, 8.339E22),
"Mn": ElementData(25, "Mn", "Manganese", 55, 54.940, 54.938, 7.4341, 8.149E22, 1.122, 2.98, 7.4341, 8.149E22),
"Fe": ElementData(26, "Fe", "Iron", 56, 55.935, 55.847, 7.8658, 8.482E22, .927, 4.34, 7.8658, 8.482E22),
"Co": ElementData(27, "Co", "Cobalt", 59, 58.930, 58.933, 8.9000, 9.095E22, 1.005, 4.43, 8.9000, 9.095E22),
"Ni": ElementData(28, "Ni", "Nickel", 58, 57.940, 58.690, 8.8955, 9.128E22, 1.200, 4.46, 8.8955, 9.128E22),
"Cu": ElementData(29, "Cu", "Copper", 63, 62.930, 63.546, 8.9200, 8.453E22, 1.066, 3.52, 8.9200, 8.453E22),
"Zn": ElementData(30, "Zn", "Zinc", 64, 63.930, 65.390, 7.1400, 6.576E22, .974, 1.35, 7.1400, 6.576E22),
"Ga": ElementData(31, "Ga", "Gallium", 69, 68.930, 69.720, 5.9040, 5.100E22, .849, 2.82, 5.9040, 5.100E22),
"Ge": ElementData(32, "Ge", "Germanium", 74, 73.920, 72.610, 5.3500, 4.437E22, .950, 3.88, 5.3500, 4.437E22),
"As": ElementData(33, "As", "Arsenic", 75, 74.920, 74.922, 5.7270, 4.603E22, 1.090, 1.26, 5.7270, 4.603E22),
"Se": ElementData(34, "Se", "Selenium", 80, 79.920, 78.960, 4.8100, 3.668E22, 1.043, 2.14, 4.8100, 3.668E22),
"Br": ElementData(35, "Br", "Bromine", 79, 78.920, 79.904, 3.1990, 2.411E22, .497, .00, 3.1990, 2.411E22),
"Kr": ElementData(36, "Kr", "Krypton", 84, 83.912, 83.800, 2.6021, 1.870E22, .378, .00, 3.740E-3, 2.689E19),
"Rb": ElementData(37, "Rb", "Rubidium", 85, 84.910, 85.470, 1.5320, 1.079E22, .352, .86, 1.5320, 1.079E22),
"Sr": ElementData(38, "Sr", "Strontium", 88, 87.910, 87.620, 2.6000, 1.787E22, .578, 1.70, 2.6000, 1.787E22),
"Y": ElementData(39, "Y", "Yttrium", 89, 88.906, 88.905, 4.4690, 3.027E22, .778, 4.24, 4.4690, 3.027E22),
"Zr": ElementData(40, "Zr", "Zirconium", 90, 89.900, 91.220, 6.4900, 4.285E22, 1.021, 6.33, 6.4900, 4.285E22),
"Nb": ElementData(41, "Nb", "Niobium", 93, 92.910, 92.906, 8.5700, 5.555E22, 1.029, 7.59, 8.5700, 5.555E22),
"Mo": ElementData(42, "Mo", "Molybdenum", 98, 97.905, 95.940, 10.2060, 6.406E22, 1.254, 6.83, 10.2060, 6.406E22),
"Tc": ElementData(43, "Tc", "Technetium", 97, 97.000, 97.000, 11.5000, 7.140E22, 1.000, .00, 11.5000, 7.140E22),
"Ru": ElementData(44, "Ru", "Ruthenium", 102, 101.904, 101.070, 12.3000, 7.329E22, 1.124, 6.69, 12.3000, 7.329E22),
"Rh": ElementData(45, "Rh", "Rhodium", 103, 102.905, 102.910, 12.3990, 7.256E22, 1.088, 5.78, 12.3990, 7.256E22),
"Pd": ElementData(46, "Pd", "Palladium", 106, 105.903, 106.400, 12.0200, 6.803E22, 1.271, 3.91, 12.0200, 6.803E22),
"Ag": ElementData(47, "Ag", "Silver", 107, 106.905, 107.870, 10.4730, 5.847E22, 1.254, 2.97, 10.4730, 5.847E22),
"Cd": ElementData(48, "Cd", "Cadmium", 114, 113.903, 112.400, 8.6420, 4.630E22, .901, 1.16, 8.6420, 4.630E22),
"In": ElementData(49, "In", "Indium", 115, 114.904, 114.820, 7.3000, 3.829E22, .741, 2.49, 7.3000, 3.829E22),
"Sn": ElementData(50, "Sn", "Tin", 120, 119.902, 118.710, 7.2816, 3.694E22, .861, 3.12, 7.2816, 3.694E22),
"Sb": ElementData(51, "Sb", "Antimony", 121, 120.903, 121.750, 6.6840, 3.306E22, .932, 2.72, 6.6840, 3.306E22),
"Te": ElementData(52, "Te", "Tellurium", 130, 129.906, 127.600, 6.2500, 2.950E22, 1.005, 2.02, 6.2500, 2.950E22),
"I": ElementData(53, "I", "Iodine", 127, 126.904, 126.900, 4.9373, 2.343E22, .554, .00, 4.9373, 2.343E22),
"Xe": ElementData(54, "Xe", "Xenon", 132, 131.904, 131.300, 3.0589, 1.403E22, .433, .00, 5.890E-3, 2.703E19),
"Cs": ElementData(55, "Cs", "Cesium", 133, 132.905, 132.910, 1.8785, 8.511E21, .326, .81, 1.8785, 8.511E21),
"Ba": ElementData(56, "Ba", "Barium", 138, 137.905, 137.327, 3.5100, 1.539E22, .513, 1.84, 3.5100, 1.539E22),
"La": ElementData(57, "La", "Lanthanum", 139, 138.906, 138.910, 6.1738, 2.676E22, .695, 4.42, 6.1738, 2.676E22),
"Ce": ElementData(58, "Ce", "Cerium", 140, 139.905, 140.120, 6.6724, 2.868E22, .726, 4.23, 6.6724, 2.868E22),
"Pr": ElementData(59, "Pr", "Praseodymium", 141, 140.907, 140.910, 6.7730, 2.895E22, .712, 3.71, 6.7730, 2.895E22),
"Nd": ElementData(60, "Nd", "Neodymium", 142, 141.907, 144.240, 7.0080, 2.926E22, .674, 3.28, 7.0080, 2.926E22),
"Pm": ElementData(61, "Pm", "Promethium", 148, 148.000, 148.000, 6.4750, 2.635E22, .714, .00, 6.4750, 2.635E22),
"Sm": ElementData(62, "Sm", "Samarium", 152, 151.919, 150.360, 7.5200, 3.012E22, .715, 2.16, 7.5200, 3.012E22),
"Eu": ElementData(63, "Eu", "Europium", 153, 152.921, 151.970, 5.2440, 2.078E22, .591, 1.85, 5.2440, 2.078E22),
"Gd": ElementData(64, "Gd", "Gadolinium", 158, 157.924, 157.250, 7.9010, 3.026E22, .703, 3.57, 7.9010, 3.026E22),
"Tb": ElementData(65, "Tb", "Terbium", 159, 158.925, 158.930, 8.2300, 3.118E22, .680, 3.81, 8.2300, 3.118E22),
"Dy": ElementData(66, "Dy", "Dysprosium", 164, 163.929, 162.500, 8.5510, 3.169E22, .682, 2.89, 8.5510, 3.169E22),
"Ho": ElementData(67, "Ho", "Holmium", 165, 164.930, 164.930, 8.7950, 3.211E22, .681, 3.05, 8.7950, 3.211E22),
"Er": ElementData(68, "Er", "Erbium", 166, 165.930, 167.260, 9.0660, 3.264E22, .685, 3.05, 9.0660, 3.264E22),
"Tm": ElementData(69, "Tm", "Thulium", 169, 168.934, 168.930, 9.3210, 3.323E22, .687, 2.52, 9.3210, 3.323E22),
"Yb": ElementData(70, "Yb", "Ytterbium", 174, 173.939, 173.040, 6.9600, 2.422E22, .619, 1.74, 6.9600, 2.422E22),
"Lu": ElementData(71, "Lu", "Lutetium", 175, 174.941, 174.970, 9.8410, 3.387E22, .718, 4.29, 9.8410, 3.387E22),
"Hf": ElementData(72, "Hf", "Hafnium", 180, 179.947, 178.490, 13.3100, 4.491E22, .830, 6.31, 13.3100, 4.491E22),
"Ta": ElementData(73, "Ta", "Tantalum", 181, 180.948, 180.950, 16.6010, 5.525E22, 1.122, 8.10, 16.6010, 5.525E22),
"W": ElementData(74, "W", "Tungsten", 184, 183.951, 183.850, 19.3500, 6.338E22, 1.238, 8.68, 19.3500, 6.338E22),
"Re": ElementData(75, "Re", "Rhenium", 187, 186.956, 186.200, 20.5300, 6.640E22, 1.045, 8.09, 20.5300, 6.640E22),
"Os": ElementData(76, "Os", "Osmium", 192, 191.961, 190.200, 22.4800, 7.118E22, 1.073, 8.13, 22.4800, 7.118E22),
"Ir": ElementData(77, "Ir", "Iridium", 193, 192.963, 192.200, 22.4210, 7.025E22, 1.095, 6.90, 22.4210, 7.025E22),
"Pt": ElementData(78, "Pt", "Platinum", 195, 194.965, 195.080, 21.4500, 6.622E22, 1.238, 5.86, 21.4500, 6.622E22),
"Au": ElementData(79, "Au", "Gold", 197, 196.967, 196.970, 19.3110, 5.904E22, 1.288, 3.80, 19.3110, 5.904E22),
"Hg": ElementData(80, "Hg", "Mercury", 202, 201.971, 200.590, 13.5462, 4.067E22, .787, .64, 13.5462, 4.067E22),
"Tl": ElementData(81, "Tl", "Thallium", 205, 204.974, 204.380, 11.8500, 3.492E22, .664, 1.88, 11.8500, 3.492E22),
"Pb": ElementData(82, "Pb", "Lead", 208, 207.977, 207.190, 11.3437, 3.297E22, .849, 2.03, 11.3437, 3.297E22),
"Bi": ElementData(83, "Bi", "Bismuth", 209, 208.980, 208.980, 9.8000, 2.824E22, .884, 2.17, 9.8000, 2.824E22),
"Po": ElementData(84, "Po", "Polonium", 210, 209.983, 210.000, 9.2511, 2.653E22, .807, 1.50, 9.2511, 2.653E22),
"At": ElementData(85, "At", "Astatine", 210, 210.000, 210.000, 10.0000, 2.868E22, .434, .00, 10.0000, 2.868E22),
"Rn": ElementData(86, "Rn", "Radon", 222, 222.000, 222.000, 9.9100, 2.688E22, .419, .00, 9.9100, 2.688E22),
"Fr": ElementData(87, "Fr", "Francium", 223, 223.000, 223.000, 10.0000, 2.700E22, .436, .00, 10.0000, 2.700E22),
"Ra": ElementData(88, "Ra", "Radium", 226, 226.000, 226.000, 5.0222, 1.338E22, .515, .00, 5.0222, 1.338E22),
"Ac": ElementData(89, "Ac", "Actinium", 227, 227.000, 227.000, 10.0000, 2.653E22, .731, .00, 10.0000, 2.653E22),
"Th": ElementData(90, "Th", "Thorium", 232, 232.038, 232.000, 11.6580, 3.026E22, .811, 5.93, 11.6580, 3.026E22),
"Pa": ElementData(91, "Pa", "Proactinium", 231, 231.036, 231.000, 15.3700, 4.007E22, 1.958, .00, 15.3700, 4.007E22),
"U": ElementData(92, "U", "Uranium", 238, 238.051, 238.030, 19.0430, 4.818E22, 1.026, 5.42, 19.0430, 4.818E22),
}