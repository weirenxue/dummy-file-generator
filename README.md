## About The Project
During the transmittion test, a large number of dummy files play a vital role in the test. This project allow you indicate any file size range and total size, and then generates dummy files for you.  

The file size distribution is uniform distribution ( **X～U[min-size, max-size]** )

## Usage
- Generate dummy files in the specified target directory `E:\dummy\`. And indicate that total dummy size is `1GB`, file min size is `1B`, file max size is `5MB`
    ```ps
    .\dfgen.exe --target-size 1GB --min-size 1B --max-size 5MB E:\dummy\
    ```
    - The target directory must be created first.
    - The target directory must be empty.
- Generate dummy files in non-empty target directory.
    ```ps
    .\dfgen.exe --target-size 1GB --min-size 1B --max-size 5MB E:\dummy\ -c
    ```
    - When option -c is set, it will clear the target directory before generating dummy files. **This option must be used carefully, the clear operation cannot be undone!**
- If the minimum size is greater than the maximum size, it will automatically swap the two values. This example has the same functionality as the previous example.
    ```ps
    .\dfgen.exe --target-size 1GB --min-size 5MB --max-size 1B E:\dummy\ -c
    ```