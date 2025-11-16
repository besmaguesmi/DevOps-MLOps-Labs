📌 Note on Project Structure



We encountered an issue where test\_model.py could not access train.py due to their placement in different directories. Since running the test script requires access to the src folder, this caused import and path-related errors.



To avoid these bugs, we decided to place both train.py and test\_model.py under the same parent directory "src". This ensures consistent access to the required modules and prevents path-resolution problems during execution.

