see `.github/workflows/publish.yaml`

conda mambabuild xarray-behave-nogui -c conda-forge -c ncb -c anaconda -c apple --python 3.7 --user ncb
conda mambabuild xarray-behave -c conda-forge -c ncb -c anaconda --python 3.7 --user ncb
conda mambabuild xarray-behave-nogui -c conda-forge -c ncb -c anaconda --python 3.8 --user ncb
conda mambabuild xarray-behave -c conda-forge -c ncb -c anaconda --python 3.8 --user ncb
conda mambabuild xarray-behave-nogui -c conda-forge -c ncb -c anaconda --python 3.9 --user ncb
conda mambabuild xarray-behave -c conda-forge -c ncb -c anaconda --python 3.9 --user ncb
