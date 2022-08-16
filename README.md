# STAIR Fast Photo Resizer

### Background: 

Since we've introduced the first bits of automation into the photo process, Adobe Photoshop has been at the heart of it. As workloads have increased and deadlines tightened, Photoshop's performance hasn't kept up. To better leverage the speed of modern computers we've gotten to the point where we need to deploy some homegrown tools. The Fast Photo Resizer is the first of those tools. 

The tool makes use of Python and the Pillow library to do all of the processing. It does not process sequentially but instead makes use of multiple processes. When the tool gets under way it generates ten worker processes and resizes the images in parallel. Running the operations in parallel provides for a huge speed up.

On a common workload of 594 photos the tool has realized the following times. As you'll notice individual CPU cores are pretty even, but once they are running in parallel they can do a tremendous amount of work. 

**Intel i5 1167G - 594 photos in 180 seconds in sequential mode**
**Intel i5 1167G - 594 photos in 49 seconds in parallel mode**

**AMD Threadripper - 594 photos in 160 seconds in sequential mode**
**AMD Threadripper - 594 photos in 11 seconds in parallel mode**

Though the use of the script we can avoid having to load and draw the image to the screen, so we can devote all of the CPU to the work at hand. I have also enabled it to add the red chip to images, this additional step adds about 5 seconds over the course of the entire run. 

### Installation: 

If you don't already have Python installed, you can get it from the Windows Store, it does not require administrative privledges to install. Follow the link below to install Python
https://www.microsoft.com/store/productId/9PJPW5LDXLZ5

After installing Python run the provided script called 'Install Pillow.ps1', this is the image library thats going to do quite a bit of the heavy lifting for us. You should see a black window appear and then disappear after a second or so. 

Enjoy!

### Usage:

To use the script is straightforward. Place the PhotoResizerMP.py file into the target folder with images and then double click it. After double clicking it, the script will detonate and get to work on the files in the current folder. It will spawn a black window that will sit for a few moments, and eventually it will print out a timer result for the job, after that you are free to close the window.  
**NOTE: THE SCRIPT WILL OVERWRITE THE ORIGINALS**

### Further Thoughts:

On line 54 of the script is a value called max_workers, it is currently set to 10 and can be adjusted to a higher value to better saturate the CPU. The results from my i5 were done with 10 workers, the Threadripper results are with 20 workers. Feel free to experiment with this value, but beware that arbitrarily raising it will often have diminishing returns. The Threadripper benchmark completely satured all of the cores with just 20 workers. 



