const double frequency = 440.0 * pow(2.0, (note_height - 1) / 12.0);
const double modulation_index = 10.0;
const double modulator_ratio = 2.0;
buffer = amplitude * sin(
	2.0 * (double)M_PI * frequency
	* (double)(note_index * samples + i) / (double)SAMPLING_FREQUENCY
	+ modulation_index * sin(
		2.0 * (double)M_PI * frequency * modulator_ratio
		* (double)(note_index * samples + i) / (double)SAMPLING_FREQUENCY
	)
);

