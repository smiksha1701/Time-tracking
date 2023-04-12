#include <cstdio>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <array>
#include <filesystem>
#include <fstream>
#include <sstream>
class MyCustomException : public std::exception {
    public:
std::string what () {
        return "Expected result and output differ\n";
    }
};
std::string exec(const char* cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&_pclose)> pipe(_popen(cmd, "r"), _pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}
int main(int argc, char* argv[]) {
    std::string path = "./Submissions/";
    std::ifstream inputFile("tests.txt");
    std::string a, b, c;
    std::string arr_a[1000],arr_b[1000],arr_c[1000];
    int i = 0;
    while (inputFile >> a>> b>> c)
    {   
        arr_a[i]=a;
        arr_b[i]=b;
        arr_c[i]=c; 
        i++;
    }
    inputFile.close();
    char buffer[100];
    for (const auto & entry : std::filesystem::directory_iterator(path)){
        std::string file_path = std::filesystem::absolute(entry.path()).string();
        std::string cmd = std::string("g++ ") + file_path + " -o test";
        std::cout<<cmd <<std::endl;
        char* char_arr = &cmd[0];
        std::cout<<exec(char_arr);
        try{
            for(int j = 0; j<1000;j++){
                cmd = std::string(".\\test.exe ") + arr_a[j] + " "+ arr_b[j];
                char* char_arr = &cmd[0];
                std::string result = exec(char_arr);
                if (result != arr_c[j]){
                    std::cout<<"RES="<<result<<" OUT="<<arr_c[j]<<std::endl;
                    throw MyCustomException();
                }
            }
        } catch (MyCustomException mce) {
                std::cout << mce.what();
        }
        
    }
    return 0;
}