#include <iostream>
#include <boost/assign.hpp>
#include <string>
#include <typeinfo>
#include <boost/any.hpp>


using boost::any_cast;

typedef boost::any Any;
typedef std::list<Any> List;



std::ostream& print_List(std::ostream& out, List& v) {
  if ( !v.empty() ) {
    out << '[';
    for( List::iterator it=v.begin();it!=v.end();) {
      if ((*it).type()==typeid(List)) {
           List value = any_cast<List>(*it);
           print_List(out,value);
      } else {
          std::string value = any_cast<std::string>(*it);
          out << value;
      }
      it++;
      if(it!=v.end())
         out << ',';

    }
    out << "]";
  }
  return out;
}

std::ostream& operator<< (std::ostream& out,  List& v) {
  return print_List(out,v);
}

void flat(List data, List& output) {
  for(List::iterator it=data.begin();it!=data.end();it++) {
      if ((*it).type()==typeid(List)) {
        List value = any_cast<List>(*it);
        flat(value,output);
      } else {
        std::string value = any_cast<std::string>(*it);
        output.push_back(value);
      }
  }
}

int main(int argc, char *argv[]) {

  List lista = boost::assign::list_of<Any> (std::string("a"));
  List listb = boost::assign::list_of<Any> (std::string("b"))(lista);
  List listc = boost::assign::list_of<Any>(std::string("c"))(listb);
  List listd = boost::assign::list_of<Any>(std::string("d"))(listc);

  List data = boost::assign::list_of<Any>(lista)(listb)(listc)(listd)(std::string("e"));

  std::cout << data << std::endl;

  List output;

  flat(data,output);
  std::cout << output << std::endl;

}
