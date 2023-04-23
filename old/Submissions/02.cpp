#include <iostream>
int function(int a, int b){
    return 5;
}
int main(int argc, char* argv[]){
    int argv1 = atoi(argv[1]);
    int argv2 = atoi(argv[2]);
    std::cout<<function(argv1, argv2);
}