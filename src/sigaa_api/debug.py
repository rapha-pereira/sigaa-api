"""."""

from src.sigaa_api.core.portal.homepage import StudentPortal


def test():
    st_portal = StudentPortal()
    classes_portal = st_portal.get_classes_portal()
    print("\nClasses:")
    print(classes_portal.get_classes())
    print("\nBody:")
    print(classes_portal.get_classes_body())
    print("\nHeader:")
    print(classes_portal.get_classes_header())


test()
