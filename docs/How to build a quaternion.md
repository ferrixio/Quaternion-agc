# How to build a quaternion

🐉 Author: Samuele Ferri (@ferrixio)

## Introduction

The [quaternion number system](https://en.wikipedia.org/wiki/Quaternion) is an extended version of the complex numbers, firstly introduced by Rowan Hamilton in 1843. A quaternion is a 4-tuple of informations $q := a + bi + cj + dk$, where $a$, $b$, $c$, $d$ are real numbers, and $i$, $j$, $k$ are the basic quaternions.

Instead of having a single imaginary part, as a complex number, quaternions have three imaginary parts, that is, there are three elements, namely $i$, $j$ and $k$, such that
$$i^2 = j^2 = k^2 = ijk = -1$$

Addition works componentwise and it is commutative, and so is the scalar multiplication.
The Hamilton product, that is the multiplication between two quaternions, follows the expression:

$$
\begin{align*}
	(a_1 + b_1i + c_1j + d_1k)*(a_2 + b_2i + c_2j + d_2k) &= a_1a_2 - b_1b_2 - c_1c_2 - d_1d_2 \\
	&+ (b_1a_2 + b_1a_2 + c_1d_2 - d_1c_2)i \\
	&+ (a_1c_2 - b_1d_2 + c_1a_2 + d_1b_2)j \\
	& + (a_1d_2 + b_1c_2 - c_1b_2 + d_1a_1)k
\end{align*}
$$

and sadly it is not commutative since $ij = k$, $ji = -k$, $jk = i$, $kj = -i$, $ki = j$, $ik = -j$.

This set is denoted with the letter $\mathbb{H}$.

## Basic construction

A quaternion can be defined in the _standard_ way using integers, floats, lists or tuples. The main constructor has six (optional) arguments:

+ **real**: a float, pre-initialized to 0, representing the real part;
+ **i_img**: a float, pre-initialized to 0, representing the first imaginary part;
+ **j_img**: a float, pre-initialized to 0, representing the second imaginary part;
+ **k_img**: a float, pre-initialized to 0, representing the third imaginary part;
+ **seq**: a list or tuple, pre-initialized to None, representing the components of the quaternion;
+ **acc**: a float, pre-initialized to 1e-13, representing the accuracy of the quaternion.

The "pre-constructor" `__new__` checks if the arguments in input are valid, else an error will raise.

The argument `seq` has the priority on the other variables. This means that

```py
Quaternion(1,2,3, seq=[-1,-2])
'Output: -1-2i'
```

After the object is constructed, it will only have two attributes in the `self` variable:

- `q`: a 4-list of the four components of the quaternion;
- `ACCURACY`: the limit of the floating point.

To get its principal elements, seven properties were added:

+ **real**, to get the real part
+ **i**, to get the first imaginary part;
+ **j**, to get the second imaginary part;
+ **k**, to get the third imaginary part;
+ **norm**, to get the euclidean norm of the quaternion as 4D-vector;
+ **vector**, to get a three dimensional array containing the three imaginary parts;
+ **rotation**, to get the rotation associated to the quaternion.

### :pencil2: From a complex number

It is possible to build a quaternion from a complex number, using the classmethod `from_complex`. It takes in input a complex number and an optional string representing which quaternionic-imaginary part the complex-j represents.

### :pencil2: From a rotation

Any 3D rotation (theta, axis=(x1, x2, x3)) is indeed a unitary quaternion (a, b, c, d), whose components are:

```py
a = cos(theta/2)
b = x1*sin(theta/2)
c = x2*sin(theta/2)
d = x3*sin(theta/2)
```

In the opposite direction, inverting the previous equations, the method fails when the real part of the quaternion is 1. In these cases, the rotation is set to $(0,(1,0,0))$.

### :pencil2: Using `random_unit()`

With this method, three numbers between 0 and 1 are randomly generated. Then, the quaternion is setted to be unitary.
To avoid floating point inaccuracy, the procedure repeats the generation until it gets an unitary quaternion. 

### :pencil2: Using `random(a,b)`

Similar to the previous one, this method generates a quaternion whose components are random float extracted with the uniform distribution in $[a,b]$. Default values are $a=-50$ and $b=50$. 
