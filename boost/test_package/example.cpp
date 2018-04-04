#include <iostream>
#include <boost/shared_ptr.hpp>
#include <boost/make_shared.hpp>


class A {
    private:
       int _x;
    public:
        A(int x): _x(x) {}
        
        int getX(){ return _x; }
       
};

int main() {
    
    boost::shared_ptr<A> x = boost::make_shared<A>(0);
    return x->getX();
}
