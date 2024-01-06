# Cs50FinalProject

# README

## Online Ads

This web application, developed in Python using Flask, SQLite3, and Bootstrap, represents a significant milestone in my programming journey. This project stands as my first substantial endeavor, marking a notable progression from my initial experiences with game development using Gamemaker to embarking on the comprehensive CS50 course at Harvard.

My journey began with CS50, where I delved into the fundamentals of programming and gained proficiency in the C language. This immersive experience laid a solid foundation and sparked my interest in exploring more advanced concepts. The introduction to Python through CS50 provided the catalyst for my foray into web development, prompting the creation of this web application.

### Key Features

- **Ad Posting:** Users can post ads across various categories, including Real Estate, Pre-Owned Cars, Home Essentials, Tech Essentials, Musical Instruments, Children's Toys, Pets, Office Furniture, Fashion & Beauty, and Games.

- **Ad Filtering:** The application empowers users to filter ads based on specific categories, offering a tailored browsing experience.

- **Advanced Search:** An advanced search functionality allows users to discover specific ads by utilizing keywords, titles, or ad descriptions.

- **User Ads Display:** Users can seamlessly view all the ads they have posted, enhancing the overall user experience.

- **User Authentication:** The inclusion of user authentication ensures secure access to features such as posting ads and viewing user-specific content.

### Image Handling with Pillow

To enhance image compatibility and streamline display, the application leverages the Pillow library to convert images stored in the database from the BLOB (Binary Large Object) format to PNG and JPEG formats.

The code snippet below illustrates the utilization of Pillow for image conversion:

```python
for ad in user_ads:
    if ad["image_data"]:
        ad["image_data"] = convert_blob_to_png(ad["image_data"])

        helpers 

        def convert_blob_to_png(blob_data):
    try:
        image = Image.open(BytesIO(blob_data))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

## Additional Functionality

The application integrates additional features, stemming from the provided code:

- **My Ads Page:** Users can peruse a dedicated page displaying all the ads they have posted, with images seamlessly converted to PNG format using the Pillow library.

- **Individual Ad Page:** Users gain access to comprehensive information about a specific ad, including additional data tailored to the ad type (Real Estate, Pre-Owned Cars, etc.).

- **Announcement Creation:** The application facilitates the creation of new ads, with users selecting the ad category from a predefined list, leading them to a specific creation page based on their selection.

## System Requirements

Before running the application, ensure the following requirements are met:

- Python
- Flask
- SQLite3
- Pillow
- Python Packages: cs50

## Environment Setup

1. Install Python requirements using the following command:

    ```bash
    pip install flask cs50 Pillow
    ```

2. Run the application using the following command:

    ```bash
    python your_app.py
    ```

   The application will be accessible at [http://localhost:5000/](http://localhost:5000/).

## Project Structure

- **app_db.db:** SQLite3 database storing information about ads, users, and associated images.

- **templates:** Contains HTML files for rendering web pages.

- **helpers.py:** Module with auxiliary functions used in the application.

- **your_app.py:** Primary file containing the source code of the Flask application.

## Future Enhancements

The ongoing evolution of the project may include:

- Refinements to the user interface for an enhanced user experience.
- Addition of more ad categories to diversify the content.
- Ongoing enhancements in security measures and data validation.

## Challenges Faced

While working on this project, I encountered some challenges that provided valuable learning experiences:

- **Scope Expansion:** The project s scope expanded beyond my initial intentions, leading to a larger and more complex application. The introduction of additional features, such as a chat functionality, became impractical within the given time frame. This highlighted the importance of careful project planning and comprehensive architecture before initiating development.

- **Time Constraints:** The time required for project completion prompted the decision to trim down certain functionalities, notably the chat feature. This emphasized the need for realistic time management and prioritization of features to meet project deadlines.

## Lessons Learned

Reflecting on these challenges, I recognize the importance of thorough planning and project architecture. Here are some key takeaways:

- **Future Planning:** When revisiting this project, I aim to organize the main structure and files more efficiently. This involves eliminating unnecessary code repetitions, managing SQLite3 calls with greater efficiency, and storing queries in separate files. Such measures will prevent unnecessary project bloating and ensure scalability.

- **Code Refactoring:** To enhance the project s maintainability, I plan to refactor the codebase to minimize redundant sections and create modular components. This will contribute to a more organized and streamlined code structure.

- **Query Management:** I intend to centralize my SQL queries in separate files, allowing for better organization and easy access. This approach minimizes redundancy and promotes a cleaner, more maintainable codebase.

## Professional Growth

The challenges faced during this project have contributed to my professional growth by emphasizing the significance of careful planning, efficient code organization, and strategic feature prioritization. Moving forward, I am committed to applying these lessons in future projects to ensure a more seamless development process.



Developed by [Paulo Henrique Moreira Rosado] - paulomoreirarosado@hotmail.com