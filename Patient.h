#ifndef PATIENT_H
#define PATIENT_H

#include <string>

/**
 * @brief Struct representing a patient record.
 */
struct Patient {
    int id;
    std::string name;
    int age;
    std::string disease;
    int priorityLevel; // Lower value indicates higher priority (critical)

    /**
     * @brief Custom comparator for the priority queue (min-heap).
     * Patients with lower priorityLevel values are served first.
     */
    struct PriorityComparator {
        bool operator()(const Patient& p1, const Patient& p2) {
            return p1.priorityLevel > p2.priorityLevel;
        }
    };
};

#endif // PATIENT_H
