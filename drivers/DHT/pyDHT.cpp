#include "common.h"

#include <boost/python.hpp>

#include <stdexcept>

extern "C" {
	DHTResult readDHT(int type, int pin);
	bool bcm2835_init();
	struct DHTResult_;
}

class DHTReader {
public:
	DHTReader()
	{
		if (!bcm2835_init()) {
			throw std::logic_error("Initialization failed!");
		}
	}

	boost::python::tuple getTemperature(int pin = 4, int type = 11) {
		DHTResult r = readDHT(type, pin);
		return boost::python::make_tuple(r.temp, r.hum);
	}

};

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(DHTReader_getTemp_overloads, DHTReader::getTemperature, 0, 2)

BOOST_PYTHON_MODULE(pyDHT) {
	using namespace boost::python;
	class_<DHTReader>("DHTReader")
	.def( init<>() )
	.def("get_temperature", &DHTReader::getTemperature, 
		DHTReader_getTemp_overloads( args("type", "pin") ) )
	;
	def("DHTInit", bcm2835_init);
	def("pyDHT", readDHT);
}

