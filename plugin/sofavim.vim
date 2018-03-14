function s:SofaGenerateComponent(namespace, motherclass, classname)

 	" Change the working directory to current location
 	:silent exe ':cd %:p:h'

	" Generate the .h class file
 	:silent exe 'e ' . a:classname . '.h'
	:silent exe '0r $HOME/.vim/bundle/sofavim/templates/component_class.h'
	:silent exe '0r $HOME/.vim/bundle/sofavim/templates/sofa_licence'
	:silent exe '%s/_COMPONENTNAME_/' . toupper(a:classname) . '/g'
	:silent exe '%s/_COMPONENTTYPE_/' . toupper(a:namespace) . '/g'
	:silent exe '%s/_MotherClass_/' . a:motherclass . '/g'
	:silent exe '%s/_componenttype_/' . a:namespace . '/g'
	:silent exe '%s/_ComponentName_/' . a:classname . '/g'
	:silent exe 'w '. a:classname . '.h'
	
	" Generate the .cpp class file
 	:silent exe 'e ' . a:classname . '.cpp'
	:silent exe '0r $HOME/.vim/bundle/sofavim/templates/component_class.cpp'
	:silent exe '0r $HOME/.vim/bundle/sofavim/templates/sofa_licence'
	:silent exe '%s/_componenttype_/' . a:namespace . '/g'
	:silent exe '%s/_ComponentName_/' . a:classname . '/g'
	:silent exe '%s/_ComponentNameClass_/' . a:classname . 'Class/g'
	:silent exe 'w '. a:classname . '.cpp'

	"TODO: Add entry in the CMakeLists.txt of the current plugin

	:silent exe 'Explore'
endfunction

command! -nargs=+ SofaGenerateComponent :call s:SofaGenerateComponent(<f-args>)
