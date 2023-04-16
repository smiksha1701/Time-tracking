#include <iostream>
#include <thread>
#include <chrono>

int main(int arcc, char** argv) {
	int x = std::atoi(argv[1]);
	int ans = 0;
	for (int i = 1; i < x; i++) {
		if (x % i == 0) ans += i;
	}
	std::this_thread::sleep_for(std::chrono::milliseconds(500));
	std::cout << ans << std::endl;
}
