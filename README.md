# Hospital Management System

A robust C++ console application designed to manage patient records efficiently using advanced data structures. This system prioritizes critical cases and ensures data persistence across sessions.

## Key Features

*   **Efficient Patient Management**: $O(1)$ time complexity for adding, searching, and discharging patients using an unordered map.
*   **Priority-Based OPD Queue**: Automatic sorting of patients based on severity using a min-heap (priority queue), ensuring critical patients are served first.
*   **Data Persistence**: Automatic file I/O operations to save and load patient records from `patients.txt`.
*   **Auto-Increment ID**: Unique patient identification managed automatically by the system.

## Project Structure

*   `main.cpp`: Entry point containing the interactive menu-driven interface.
*   `HospitalSystem.h/cpp`: Core logic and data structure implementations.
*   `Patient.h`: Definition of the Patient record and priority comparator.
*   `patients.txt`: Data file for persistent storage (created automatically).

## Getting Started

### Prerequisites
*   A C++ compiler supporting C++17 or higher (e.g., `g++` or `clang`).

### Compilation
Use the following command to compile the project:
```bash
g++ -std=c++17 main.cpp HospitalSystem.cpp -o hospital
```

### Execution
Run the compiled executable:
```bash
./hospital
```

## Usage
1.  **Add Patient**: Register a new patient with their name, age, disease, and priority (1 for critical, 5 for normal).
2.  **Search Patient**: Quickly find patient details using their unique ID.
3.  **Discharge Patient**: Remove a patient from the system records.
4.  **Serve Next Patient**: Automatically retrieves and removes the highest priority patient from the OPD queue.
5.  **Exit**: Safely closes the application and saves all data to the disk.
