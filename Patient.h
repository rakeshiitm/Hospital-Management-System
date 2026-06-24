#ifndef PATIENT_H
#define PATIENT_H

#include <string>
struct Patient {
    int id;
    std::string name;
    int age;
    std::string disease;
    int priorityLevel;
    struct PriorityComparator {
        bool operator()(const Patient& p1, const Patient& p2) {
            return p1.priorityLevel > p2.priorityLevel;
        }
    };
};

#endif
