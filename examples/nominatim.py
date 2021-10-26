import wrapy

Location=wrapy.WraPy('https://nominatim.openstreetmap.org/search/',num_retries=3,main_args=['q'],args_required=True,format='xml')
