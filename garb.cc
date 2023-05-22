#include <bits/stdc++.h>

int main(int argc, char** argv) {
	std::clock_t start = std::clock();
	uint64_t x = 1234567891; // default value
	if (argc > 1) {
		x = std::atoll(argv[1]);
	}
	uint64_t ans = 0;
	for (uint64_t i = 1; i < x; i++) {
		if (x % i == 0) ans += 1;
	}
	// std::this_thread::sleep_for(std::chrono::milliseconds(500));
	std::cerr << ans << std::endl;
	long double time = 1000.0 * (std::clock() - start) / CLOCKS_PER_SEC;
	std::cout << time << std::endl;
}

