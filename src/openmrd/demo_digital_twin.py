# This file pulls together the full workflow of initializing a package and validating the manifest, using the c_type_permanent template as an example. 
# It serves as a demo of how to use the openmrd library to create a digital twin of an MRI scanner, and can be adapted for other templates or custom configurations.
# The steps are:
# 1. Definition - Import the scanner.yaml file 
# 2. Magnet- Obtain B0 maps 
# 3. Passive shimming - Improve the B0 maps using the outcomes from the passive shimming definition
# 4. Gradients - Obtain the gradient field maps, linearity, efficiency from the gradient definition
# 5. RF - Obtain the B1 maps, SNR, and other relevant parameters from the RF definition
# 6. Console - Obtain the calibration and imaging pulse sequences used, and other relevant parameters from the console definition - generate seq files for the pulse sequences
# 7. Phantom - Use the numerical or ex vivo phantom definition to generate the expected raw data for the defined pulse sequences, using the B0, B1 and gradient field maps obtained in the previous steps - ISMRMRD
# 8. Reconstruction - Generate the reconstructed images from the simulated raw data using the reconstruction pipeline definition, and compare with expected outcomes if available in the manifest