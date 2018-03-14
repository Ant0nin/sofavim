#include "_ComponentName_.h"

namespace sofa {

 namespace component {

  namespace _componenttype_ {

   SOFA_DECL_CLASS(_ComponentName_)

   int _ComponentNameClass_ = sofa::core::RegisterObject("_ComponentDescription_")
#ifdef SOFA_WITH_DOUBLE
.add<_ComponentName_< sofa::defaulttype::_DefaultTypeDouble_> >(true)
#endif
#ifdef SOFA_WITH_FLOAT
.add<_ComponentName_< sofa::defaulttype::_DefaultTypeFloat_> >()
#endif
;

#ifdef SOFA_WITH_DOUBLE
   template class _ComponentName_<sofa::defaulttype::_DefaultTypeDouble_>;
#endif
#ifdef SOFA_WITH_FLOAT
   template class _ComponentName_<sofa::defaulttype::_DefaultTypeFloat_>;
#endif

  }
 }
}
