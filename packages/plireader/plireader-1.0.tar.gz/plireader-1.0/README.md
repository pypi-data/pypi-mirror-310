# PLIreader
A simple .pli files reader for Abrio(tm) microbirefringence analysis system

## Usage
The only function is 'read_pli'.

Arguments are: (path, ishape=(1024, 1392)), where path is path to .pli file and ishape is shape of image (rows, columns)

Function returns: (ret, az) - numpy arrays of retardance and azimuth data with shape 'ishape'.
