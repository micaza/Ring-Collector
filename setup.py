import cx_Freeze

executables = [cx_Freeze.Executable("Main.py")]

cx_Freeze.setup(
	name="Ring_Collector",
	options={"build_exe":{"packages":["pygame"],"include_files":["clear.png","dead.wav","hero.png","hero_dead1.png","nextstage.wav","points.wav","ring.png","spike.png"]}},
	description = "Ring Collector game by Marcos Icaza 2015",
	executables = executables
	)