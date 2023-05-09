#include <bits/stdc++.h>

int main(int arcc, char** argv) {
	std::clock_t start = std::clock();
	int x = std::atoi(argv[1]);
	int ans = 0;
	for (int i = 1; i < x; i++) {
		if (x % i == 0) ans += i;
	}
	//std::this_thread::sleep_for(std::chrono::milliseconds(500));
	std::cerr << ans << std::endl;
	long double time = 1000.0 * (std::clock() - start) / CLOCKS_PER_SEC;
	std::cout << time << std::endl;
}
