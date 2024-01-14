#include <iostream>
#include<string>
using namespace std;
const int numOfBedrooms = 3;


int main() {
  int x = 0;
  cout << "Hello World!" << endl;
  cout << "Testing newline \n" << endl;
  cout << "Enter an int: ";
  cin >> x;

  //int, float, double, char, string, bool
  int myNum = 15;
  bool open = true;
  bool locked = true; //false;
  bool free = open & !locked;
  if (free){
    cout <<  "You entered " << x << endl;
  }

  return 0;
}
