#ifndef SOFA_COMPONENT__COMPONENTTYPE___COMPONENTNAME__H
#define SOFA_COMPONENT__COMPONENTTYPE___COMPONENTNAME__H

#include <sofa/core/ObjectFactory.h>

namespace sofa {

 namespace component {

  namespace _componenttype_ {

   template<typename DataTypes>
   class _ComponentName_ : public sofa::component::_componenttype_::_MotherClass_<DataTypes>
   {
    public:

     SOFA_CLASS( SOFA_TEMPLATE(_ComponentName_, DataTypes), SOFA_TEMPLATE(sofa::component::_componenttype_::_MotherClass_, DataTypes) );

     // TODO: complete class definition
   };

  }
 }
}

#endif
