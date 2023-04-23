#include <iostream>
#include <chrono>
#include <thread>
int function(int a, int b){
    std::this_thread::sleep_for(std::chrono::milliseconds(5000));
    return a+b;
}
int main(int argc, char* argv[]){
    int argv1 = atoi(argv[1]);
    int argv2 = atoi(argv[2]);
    std::cout<<function(argv1, argv2);
}