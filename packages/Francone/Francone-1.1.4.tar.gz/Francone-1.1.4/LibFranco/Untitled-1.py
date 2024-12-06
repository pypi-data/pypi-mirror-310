import numpy as np
import tdms_grafico as fd

# Esempio di utilizzo:
time = np.linspace(0, 10, 100)
dsr1 = np.sin(time)

tdms_handler = fd.TDMS('test.tdms')
spos=tdms_handler.col("*Group1*Time*")
a=fd.GRAFICO('titolo',(20,10))
a.plot([spos,spos],'label','red')
fd.TDMS().scrivi_tdms('output.tdms',(time, 'Group_Time', 'Time'),(dsr1, 'Group_Time', 'dsr1'),(dsr1, 'Group_dsr', 'dsr1'))
