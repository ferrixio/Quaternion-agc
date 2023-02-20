/*
Quaternion class for C++

Author:     Samuele Ferri (@ferrixio)
Version:    1.0
*/

#include <iostream>
#include <cmath>
#include <cstdio>
#include <string>

typedef std::numeric_limits< double > dbl;


class Quaternion{

    private:
    double real, i, j, k;
    
    public:
    Quaternion(double real_part=0, double i_img=0, double j_img=0, double k_img=0){
        real = real_part, i = i_img, j = j_img, k = k_img;}

    double get_real(){return real;}

    double get_i(){return i;}

    double get_j(){return j;}

    double get_k(){return k;}

    double square_norm(){
        /*Evaluates the square norm of the quaternion*/
        return real*real + i*i + j*j + k*k;}

    double norm(){
        /*Evaluates the norm of the quaternion*/
        return pow(square_norm(), 0.5);}



    // Algebruh
    Quaternion inverse(){
        /*Returns the inverse quaternion*/
        double n2 = square_norm();
        if (n2 <= 1e-15){throw std::domain_error("Zero division error");}
        return Quaternion(real/n2, -i/n2, -j/n2, -k/n2);
    }

    Quaternion inverse_ip(){
        /*Inverts the quaternion*/
        double n2 = square_norm();
        if (n2 <= 1e-15){throw std::domain_error("Zero division error");}
        real /= n2, i /= -n2, j /= -n2, k /= -n2;
        return *this;
    }

    Quaternion conjugate() {
        /*Returns the conjugated quaternion*/
        return Quaternion(real, -i, -j, -k);
    }

    Quaternion conjugate_ip() {
        /*Conjugates the quaternion*/
        i *= -1, j *= -1, k *= -1;
        return *this;
    }

    Quaternion normalize() {
        /*Returns the normalized quaternion*/
        double n = norm();
        if (n <= 1e-15){throw std::domain_error("Zero division error");}
        if (n != 1.0){return Quaternion(real/n, i/n, j/n, k/n);}
    }

    Quaternion normalize_ip(){
        /*Normalizes the quaternion*/
        double n = norm();
        if (n <= 1e-15){throw std::domain_error("Zero division error");}
        if (n != 1.0){
            real /= n, i /= n, j /= n, k /= n;
            return *this;
        }
    }



    // Conversions
    int to_int(){
        /*Conversion quaternion -> int*/
        return int(real);}

    float to_float(){
        /*Conversion quaternion -> float*/
        return float(real);}

    double to_double(){
        /*Conversion quaternion -> double*/
        return double(real);}



    // Bitwise operators
    friend std::ostream &operator << (std::ostream &output, Quaternion const &obj) {
        /*Overloading cout statement*/
        output << obj.real << (obj.i>=0 ? "+" : "") << obj.i << "i" << \
                    (obj.j>=0 ? "+" : "") << obj.j << "j" << \
                    (obj.k>=0 ? "+" : "") << obj.k << "k\t";
        return output;
    }

    Quaternion operator + (){
        /*Overloading +x operator*/
        return Quaternion(real,i,j,k);}

    Quaternion operator - (){
        /*Overloading -x operator*/
        return Quaternion(-real, -i, -j, -k);}

    Quaternion operator ~(){
        /*Overloading ~x operator == get inverse quaternion*/
        return inverse();}

    

    // Boolean methods
    Quaternion& operator = (Quaternion const &obj)& {
        real = obj.real;
        i = obj.i, j = obj.j, k = obj.k;
        return *this;}

    bool operator == (Quaternion const &obj) {
        /*Boolean check x == y*/
        return (*this-obj).norm() <= 1e-15;}

    bool operator != (Quaternion const &obj) {
        /*Boolean check !=*/
        return (*this-obj).norm() > 1e-15;}

    bool is_unit(){
        /*Checks if the quaternion is unitary*/
        return square_norm() == 1.0;}

    bool is_real(){
        /*Checks if the quaternion is a real number*/
        return i <= 1e-15 && j <= 1e-15 && k <= 1e-15;}

    bool is_imagy(){
        /*Checks if the quaternion has only imaginary parts*/
        return real <= 1e-15 && (i!=0 || j!=0 || k!=0);}
 
    

    // Binary operations
    // Sum
    Quaternion& operator += (Quaternion const &obj)& {
        /*Overloading of += : H x H -> H */
        real += obj.real, i+=obj.i, j+=obj.j, k+=obj.k;
        return *this;
    }

    friend Quaternion operator + (Quaternion self, Quaternion const &obj) {
        /*Overloading of + : H x H -> H */
        return self += obj;}

    // Subtraction
    Quaternion& operator -= (Quaternion const &obj)& {
        /*Overloading of -= : H x H -> H */
        real -= obj.real, i-=obj.i, j-=obj.j, k-=obj.k;
        return *this;
    }

    friend Quaternion operator - (Quaternion self, Quaternion const &obj) {
        /*Overloading of - : H x H -> H */
        return self -= obj;}    

    // Multiplications
    Quaternion& operator *= (Quaternion const &obj)& {
        /*Overloading of *= : H x H -> H */
        double n_real = real*obj.real - i*obj.i - j*obj.j - k*obj.k;
        double n_i = real*obj.i + i*obj.real + j*obj.k - k*obj.j;
        double n_j = real*obj.j + j*obj.real - i*obj.k + k*obj.i;
        double n_k = real*obj.k + k*obj.real + i*obj.j - j*obj.i;

        real = n_real, i = n_i, j = n_j, k = n_k;
        return *this;
    }

    friend Quaternion operator * (Quaternion self, Quaternion const &obj) {
        /*Overloading * : H x H -> H */
        return self *= obj;}

    // Divisions
    Quaternion& operator /= (Quaternion obj)& {
        /*Overloading of /= : H x H -> H */
        obj.inverse_ip();
        double n_real = real*obj.real - i*obj.i - j*obj.j - k*obj.k;
        double n_i = real*obj.i + i*obj.real + j*obj.k - k*obj.j;
        double n_j = real*obj.j + j*obj.real - i*obj.k + k*obj.i;
        double n_k = real*obj.k + k*obj.real + i*obj.j - j*obj.i;

        real = n_real, i = n_i, j = n_j, k = n_k;
        return *this;
    }

    friend Quaternion operator / (Quaternion self, Quaternion obj) {
        /*Overloading of / : H x H -> H */
        return self /= obj;}

};


int main(){
    Quaternion x(0,1,1,1), y(1,-1,1,4);

    std::cout << (x/y) << (y/x) << std::endl;
    return 0;
}