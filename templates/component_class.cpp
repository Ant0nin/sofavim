#include "_ComponentName_.h"

namespace sofa {

 namespace component {

  namespace _componenttype_ {

   SOFA_DECL_CLASS(_ComponentName_)

   int _ComponentNameClass_ = sofa::core::RegisterObject("This force field applies the atmospheric pressure onto the target object").add<_ComponentName_>(true);

   // TODO: complete class behavior
  }
 }
}
