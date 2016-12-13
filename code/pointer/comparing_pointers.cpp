bool MeiElement::hasChild(MeiElement *child) {
    for (vector<MeiElement*>::iterator iter = _children.begin(); iter != _children.end(); ++iter) {
        if((&child) == &(*iter)) {
            return true;
        }
    }
    return false;
}
