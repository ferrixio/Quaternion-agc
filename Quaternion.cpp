/*
Quaternion class for C++

Author:     Samuele Ferri (@ferrixio)
Version:    1.0.1
*/
#define _USE_MATH_DEFINES

#include <iostream>
#include <cmath>
#include <cstdio>
#include <string>
#include <ctime>

typedef std::numeric_limits< double > dbl;


class Quaternion{

    private:
    double real, i, j, k;
    
    public:
    /*Standard initializer*/
    Quaternion(double real_part=0, double i_img=0, double j_img=0, double k_img=0){
        real = real_part, i = i_img, j = j_img, k = k_img;}


    double get_real(){return real;}

    double get_i(){return i;}

    double get_j(){return j;}

    double get_k(){return k;}



    // Conversions
    /*Conversion quaternion -> int*/
    int to_int(){return static_cast<int>(real);}

    /*Conversion quaternion -> float*/
    float to_float(){return static_cast<float>(real);}

    /*Conversion quaternion -> double*/
    double to_double(){return static_cast<double>(real);}



    // Bitwise operators
    /*Overloading of cout statement*/
    friend std::ostream &operator << (std::ostream &output, Quaternion const &obj) {
        std::cout.precision(dbl::max_digits10);
        output << obj.real << (obj.i>=0 ? "+" : "") << obj.i << "i" << \
                    (obj.j>=0 ? "+" : "") << obj.j << "j" << \
                    (obj.k>=0 ? "+" : "") << obj.k << "k\n";
        return output;
    }

    /*Overloading of +x operator*/
    Quaternion operator + (){return Quaternion(real,i,j,k);}

    /*Overloading of -x operator*/
    Quaternion operator - (){return Quaternion(-real, -i, -j, -k);}

    /*Overloading of ~x operator to get the inverse quaternion*/
    Quaternion operator ~(){return inverse();}

    

    // Boolean methods
    /*Overloading = operator to variable assignment*/
    Quaternion& operator = (Quaternion const &obj)& {
        real = obj.real;
        i = obj.i, j = obj.j, k = obj.k;
        return *this;}

    /*Boolean check x == y*/
    bool operator == (Quaternion const &obj) {return (*this-obj).norm() <= 1e-15;}

    /*Boolean check x != y*/
    bool operator != (Quaternion const &obj) {return (*this-obj).norm() > 1e-15;}

    /*Checks if the quaternion is unitary*/
    bool is_unit(){return square_norm() == 1.0;}

    /*Checks if the quaternion is a real number*/
    bool is_real(){return i <= 1e-15 && j <= 1e-15 && k <= 1e-15;}

    /*Checks if the quaternion has only imaginary parts*/
    bool is_imagy(){return real <= 1e-15 && (i!=0 || j!=0 || k!=0);}
 
    

    // Binary operations
    /*Overloading of += : H x H -> H */
    Quaternion& operator += (Quaternion const &obj)& {
        real += obj.real, i+=obj.i, j+=obj.j, k+=obj.k;
        return *this;
    }

    /*Overloading of + : H x H -> H */
    friend Quaternion operator + (Quaternion self, Quaternion const &obj) {return self += obj;}

    /*Overloading of -= : H x H -> H */
    Quaternion& operator -= (Quaternion const &obj)& {
        real -= obj.real, i-=obj.i, j-=obj.j, k-=obj.k;
        return *this;
    }

    /*Overloading of - : H x H -> H */
    friend Quaternion operator - (Quaternion self, Quaternion const &obj) {return self -= obj;}    

    /*Overloading of *= : H x H -> H */
    Quaternion& operator *= (Quaternion const &obj)& {
        double n_real = real*obj.real - i*obj.i - j*obj.j - k*obj.k;
        double n_i = real*obj.i + i*obj.real + j*obj.k - k*obj.j;
        double n_j = real*obj.j + j*obj.real - i*obj.k + k*obj.i;
        double n_k = real*obj.k + k*obj.real + i*obj.j - j*obj.i;

        real = n_real, i = n_i, j = n_j, k = n_k;
        return *this;
    }

    /*Overloading * : H x H -> H */
    friend Quaternion operator * (Quaternion self, Quaternion const &obj) {return self *= obj;}

    /*Overloading of /= : H x H -> H */
    Quaternion& operator /= (Quaternion obj)& {
        obj.inverse_ip();
        double n_real = real*obj.real - i*obj.i - j*obj.j - k*obj.k;
        double n_i = real*obj.i + i*obj.real + j*obj.k - k*obj.j;
        double n_j = real*obj.j + j*obj.real - i*obj.k + k*obj.i;
        double n_k = real*obj.k + k*obj.real + i*obj.j - j*obj.i;

        real = n_real, i = n_i, j = n_j, k = n_k;
        return *this;
    }

    /*Overloading of / : H x H -> H */
    friend Quaternion operator / (Quaternion self, Quaternion obj) {return self /= obj;}



    // Algebruh
    /*Evaluates the square norm of the quaternion*/
    double square_norm(){return real*real + i*i + j*j + k*k;}

    /*Evaluates the norm of the quaternion*/
    double norm(){return pow(square_norm(), 0.5);}
    
    /*Returns the inverse quaternion*/
    Quaternion inverse(){
        double n2 = square_norm();
        if (n2 <= 1e-15){throw std::domain_error("Zero division error");}
        return Quaternion(real/n2, -i/n2, -j/n2, -k/n2);}

    /*Inverts the quaternion*/
    Quaternion inverse_ip(){
        double n2 = square_norm();
        if (n2 <= 1e-15){throw std::domain_error("Zero division error");}
        real /= n2, i /= -n2, j /= -n2, k /= -n2;
        return *this;}

    /*Returns the conjugated quaternion*/
    Quaternion conjugate() {return Quaternion(real, -i, -j, -k);}

    /*Conjugates the quaternion*/
    Quaternion conjugate_ip() { 
        i *= -1, j *= -1, k *= -1;
        return *this;}

    /*Returns the normalized quaternion*/
    Quaternion normalize() {
        double n = norm();
        if (n <= 1e-15){throw std::domain_error("Zero division error");}
        if (n != 1.0){return Quaternion(real/n, i/n, j/n, k/n);}}

    /*Normalizes the quaternion*/
    Quaternion normalize_ip(){
        double n = norm();
        if (n <= 1e-15){throw std::domain_error("Zero division error");}
        if (n != 1.0){
            real /= n, i /= n, j /= n, k /= n;
            return *this;
        }}



};


int main(){
    Quaternion x(0,1,1,1), y(1,-1,1,4);
    std::cout << (x/y) << (y/x) << std::endl;
}