#ifndef MyObject_h
#define MyObject_h

#include <TObject.h>

class MyObject : public TObject {
  UInt_t m_run;
  UInt_t m_event;
 public:
  void set_run(const UInt_t& r) {m_run = r;}
  void set_event(const UInt_t& e) {m_event = e;}

  UInt_t get_run() const {return m_run;}
  UInt_t get_event() const {return m_event;}

  ClassDef(MyObject,1)
    };

ClassImp(MyObject)

#endif
