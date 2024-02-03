from repoManager.utils import extract_file_name


def test_extract_file_name():
   """
   Given emptry file system
   When get_images called
   Then return no results
   """

   # Arrange

   # Act
   time, prompt = extract_file_name("21:13:06.642930_Bees____")
   
   # Assert
   assert time == "21:13:06.642930"
   assert prompt == "Bees____"