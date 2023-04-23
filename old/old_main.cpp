#include <iostream>
#include <math.h>
#include <iomanip>
#include <ctime>
#include <cstdlib>
#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif 

void garbage_pi_calc(long long n, clock_t start){
    clock_t now;
    int sign = 1;
    double sum = 0.0;
    double pi = 0; 
    int i = 1;
    float seconds = n*60;
    while(((now - start) / CLOCKS_PER_SEC) <= seconds){
        sum += sign/(2.0*i+1.0);
        sign *= -1;
        i++;
        now = clock();
    }
}
double sleep_func(long long n){
    Sleep(n); 
    return 0;
}
int main(int argc, char* argv[]) {
    long long n = 0;
    
    std::string argv1 = argv[1];
    int argv2 = atoi(argv[2]);
    if (argv1 == "-help"){
        std::cout<<"-help : display this text \n-run : select how to run this program:"<<
        "\n arg1 = 1 : Run garbage calculations for arg2 milliseconds"<<
        "\n arg1 = 2 : Sleep for arg2 milliseconds\n";
    }
    if (argv1 == "-run"){
        if (argv2 > 0 && argv2 < 3){
            n = atoi(argv[3]);
        }
    }
    clock_t start = clock();
    if (argv2 == 1){
        
        garbage_pi_calc(n, start);
    }
    else{
        sleep_func(n);
    }
    clock_t now = clock();
    std::cout<<"\nProcess terminated after "<< ((now - start) / CLOCKS_PER_SEC);
}