import React, { useState, useEffect } from 'react';
import { getCookie } from '../../utils/csrf';

export default function ViewPets() {
    const [pets, setPets] = useState([]);
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [servicesLoading, setServicesLoading] = useState(false);
    const [selectedPet, setSelectedPet] = useState(null);
    const [showPetModal, setShowPetModal] = useState(false);
    const [activeTab, setActiveTab] = useState('details'); // 'details' or 'services'
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [petToDelete, setPetToDelete] = useState(null);
    const [editForm, setEditForm] = useState({
        petName: '',
        petColor: '',
        breed: '',
        species: '',
        birthDay: '',
        age: '',
        sex: '',
        remarks: ''
    });

    useEffect(() => {
        fetchUserPets();
    }, []);

    // Real-time age calculation function (same as desktop)
    const calculateAge = (birthday) => {
        if (!birthday) return '';

        const today = new Date();
        const birthDate = new Date(birthday);
        const days = Math.floor((today - birthDate) / (1000 * 60 * 60 * 24));

        if (days < 0) return '0 days old';

        if (days < 7) {
            return `${days} day${days !== 1 ? 's' : ''} old`;
        } else if (days < 30) {
            const weeks = Math.floor(days / 7);
            return `${weeks} week${weeks !== 1 ? 's' : ''} old`;
        } else if (days < 365) {
            const months = Math.floor(days / 30);
            return `${months} month${months !== 1 ? 's' : ''} old`;
        } else {
            const years = Math.floor(days / 365);
            return `${years} year${years !== 1 ? 's' : ''} old`;
        }
    };

    const fetchUserPets = async () => {
        try {
            const res = await fetch('/api/pets/', {
                credentials: 'include',
                headers: {
                  'X-CSRFToken': getCookie('csrftoken') || ''
                }
            });

            if (res.ok) {
                const petsData = await res.json();
                setPets(petsData);
            }
            else {
                console.error('Failed to fetch pets');
            }
        }
        catch (error) {
            console.error('Error fetching pets:', error);
        }
        finally {
            setLoading(false);
        }
    };
    const fetchPetServices = async (petId) => {
        setServicesLoading(true);
        try {
            const res = await fetch(`/api/services/?pet_id=${petId}`, {
                credentials: 'include',
                headers: {
                  'X-CSRFToken': getCookie('csrftoken') || ''
                }
            });

            if (res.ok) {
                const servicesData = await res.json();
                setServices(servicesData);
            } else {
                console.error('Failed to fetch services');
                setServices([]);
            }
        } catch (error) {
            console.error('Error fetching services:', error);
            setServices([]);
        } finally {
            setServicesLoading(false);
        }
    };

    const openPetModal = (pet) => {
        setSelectedPet(pet);
        setShowPetModal(true);
        setActiveTab('details');
        // Pre-fetch services for this pet
        fetchPetServices(pet.id);
    };

    const closePetModal = () => {
        setSelectedPet(null);
        setShowPetModal(false);
        setServices([]);
    };

    const handleTabClick = (tab) => {
        setActiveTab(tab);
        // If switching to services tab and services aren't loaded yet, fetch them
        if (tab === 'services' && selectedPet && services.length === 0) {
            fetchPetServices(selectedPet.id);
        }
    };

    const openEditModal = (pet) => {
        setEditForm({
            petName: pet.petName || '',
            petColor: pet.petColor || '',
            breed: pet.breed || '',
            species: pet.species || '',
            birthDay: pet.birthDay || '',
            age: pet.age || '',
            sex: pet.sex || '',
            remarks: pet.remarks || ''
        });
        setShowEditModal(true);
        setShowPetModal(false);
    };

    const closeEditModal = () => {
        setShowEditModal(false);
        setEditForm({
          petName: '',
          petColor: '',
          breed: '',
          species: '',
          birthDay: '',
          age: '',
          sex: '',
          remarks: ''
        });
    };

    const handleEditChange = (e) => {
        const { name, value } = e.target;

        setEditForm(prev => {
            const updatedForm = {
                ...prev,
                [name]: value
            };

            // Real-time age calculation when birthday changes
            if (name === 'birthDay' && value) {
                updatedForm.age = calculateAge(value);
            }

            return updatedForm;
        });
    };

    const handleAgeChange = (e) => {
        const { value } = e.target;

        // If user manually types in age, clear the birthday
        setEditForm(prev => ({
            ...prev,
            age: value,
            birthDay: value ? '' : prev.birthDay // Clear birthday if age is manually entered
        }));
    };

    const handleEditSubmit = async (e) => {
        e.preventDefault();

        if (!selectedPet) return;

        try {
            const res = await fetch(`/api/pets/${selectedPet.id}/`, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken') || ''
                },
                credentials: 'include',
                body: JSON.stringify({
                  ...editForm,
                  // Ensure stored_age is only sent if no birthday
                  stored_age: editForm.birthDay ? null : (editForm.age || null)
                })
            });

            if (res.ok) {
                const updatedPet = await res.json();
                // Update the pet in local state
                setPets(pets.map(pet =>
                  pet.id === selectedPet.id ? updatedPet : pet
                ));
                alert('Pet updated successfully!');
                closeEditModal();
                closePetModal();
            } else {
                throw new Error('Failed to update pet');
            }
        }
        catch (error) {
            console.error('Error updating pet:', error);
            alert('Error updating pet. Please try again.');
        }
    };

    const handleDeleteClick = (pet) => {
        setPetToDelete(pet);
        setShowDeleteConfirm(true);
    };

    const confirmDelete = async () => {
        if (!petToDelete) return;

        try {
            const res = await fetch(`/api/pets/${petToDelete.id}/`, {
                method: 'DELETE',
                headers: {
                  'X-CSRFToken': getCookie('csrftoken') || ''
                },
                credentials: 'include'
            });

            if (res.ok) {
                // Remove pet from local state
                setPets(pets.filter(pet => pet.id !== petToDelete.id));
                alert('Pet deleted successfully!');

                // Close both modals
                setShowDeleteConfirm(false);
                closePetModal();
            }
            else {
                throw new Error('Failed to delete pet');
            }
        }
        catch (error) {
            console.error('Error deleting pet:', error);
            alert('Error deleting pet. Please try again.');
        }
        finally {
            setPetToDelete(null);
        }
    };

    const cancelDelete = () => {
        setPetToDelete(null);
        setShowDeleteConfirm(false);
    };

    const getSpeciesIcon = (species) => {
        const speciesLower = species?.toLowerCase();
        if (speciesLower === 'dog') return '/assets/icons/dog.png';
        if (speciesLower === 'cat') return '/assets/icons/catIcon.png';
        return '/assets/icons/otherSpecies.png';
    };

    const formatDate = (dateString) => {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);

        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    };

    const getStatusBadge = (status) => {
        const statusConfig = {
            'pending': { class: 'status-pending', text: 'Pending' },
            'completed': { class: 'status-completed', text: 'Completed' },
            'overdue': { class: 'status-overdue', text: 'Overdue' },
            'cancelled': { class: 'status-cancelled', text: 'Cancelled' }
        };

        const config = statusConfig[status] || { class: 'status-pending', text: status };
        return <span className={`status-badge ${config.class}`}>{config.text}</span>;
    };

    if (loading) {
        return (
            <div className="view-pets-container">
                <div className="loading">Loading pets...</div>
            </div>
        );
    }

  return (
    <div className="view-pets-container">
      <div className="pets-header">
        <h1>My Pets</h1>
        <p>Manage and view your pet records</p>
      </div>

      {pets.length === 0 ? (
        <div className="empty-state">
          <img src="/assets/icons/no-pets.png" alt="No pets" className="empty-icon" />
          <h3>No Pets Yet</h3>
          <p>Add your first pet to get started</p>
        </div>
      ) : (
        <div className="pets-grid">
          {pets.map((pet) => (
            <div
              key={pet.id}
              className="pet-card"
              onClick={() => openPetModal(pet)}
            >
              <div className="pet-card-header">
                <img
                  src={getSpeciesIcon(pet.species)}
                  alt={pet.species}
                  className="pet-icon"
                />
                <h3 className="pet-name">{pet.petName}</h3>
              </div>

              <div className="pet-details">
                <div className="pet-detail">
                  <span className="label">Breed:</span>
                  <span className="value">{pet.breed}</span>
                </div>
                <div className="pet-detail">
                  <span className="label">Color:</span>
                  <span className="value">{pet.petColor}</span>
                </div>
                <div className="pet-detail">
                  <span className="label">Age:</span>
                  <span className="value">{pet.age || 'Unknown'}</span>
                </div>
                <div className="pet-detail">
                  <span className="label">Sex:</span>
                  <span className="value">{pet.sex}</span>
                </div>
              </div>

              {pet.has_reminder && (
                <div className="reminder-badge">
                  ⏰ Has Reminder
                </div>
              )}
            </div>
          ))}
        </div>
      )}


      {showPetModal && selectedPet && (
        <div className="modal-overlay" onClick={closePetModal}>
          <div className="pet-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
               <div className="modal-tabs">
                   <button
                        className={`tab ${activeTab === 'details' ? 'active' : ''}`}
                        onClick={() => handleTabClick('details')}
                        > Details
                    </button>
                   <button
                       className={`tab ${activeTab === 'services' ? 'active' : ''}`}
                       onClick={() => handleTabClick('services')}
                       >Service History
                   </button>
               </div>
              <button className="close-btn" onClick={closePetModal}>×</button>
            </div>
            {activeTab === 'details' &&(
                <div className="details-container">
                    <div className="pet-profile-header">
                        <img
                        src={getSpeciesIcon(selectedPet.species)}
                        alt={selectedPet.species}
                        className="profile-pet-icon"
                        />
                        <div className="pet-profile-info">
                            <h1>{selectedPet.petName}</h1>
                            <p className="pet-breed">{selectedPet.breed}</p>
                        </div>
                    </div>

                    <div className="details-grid">
                        <div className="detail-section">
                            <h3>Basic Information</h3>
                            <div className="detail-row">
                                <span className="detail-label">Species:</span>
                                <span className="detail-value">{selectedPet.species}</span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label">Color:</span>
                                <span className="detail-value">{selectedPet.petColor}</span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label">Sex:</span>
                                <span className="detail-value">{selectedPet.sex}</span>
                            </div>
                        </div>

                        <div className="detail-section">
                            <h3>Age Information</h3>
                                <div className="detail-row">
                                <span className="detail-label">Birthday:</span>
                                <span className="detail-value">
                                {selectedPet.birthDay ? formatDate(selectedPet.birthDay) : 'Not specified'}
                                </span>
                            </div>

                            <div className="detail-row">
                                <span className="detail-label">Age:</span>
                                <span className="detail-value">{selectedPet.age || 'Unknown'}</span>
                            </div>
                        </div>

                        {selectedPet.remarks && (
                        <div className="detail-section">
                            <h3>Remarks</h3>
                            <p className="remarks-text">{selectedPet.remarks}</p>
                        </div>
                        )}
                    </div>

                    <div className="modal-actions">
                        <button
                            className="DeletePetBtn"
                            onClick={() => handleDeleteClick(selectedPet)}
                            >DELETE PET
                        </button>

                        <button
                            className="EditPetBtn"
                            onClick={() => openEditModal(selectedPet)}
                            >EDIT PET
                        </button>
                    </div>
                </div>
            )}

            {activeTab === 'services' && (
                <div className="services-container">
                    <div className="services-header">
                        <h3>Service History for {selectedPet.petName}</h3>
                        <p>All medical services and appointments</p>
                    </div>

                    {servicesLoading ? (
                        <div className="loading">Loading services...</div>
                    ) : services.length === 0 ? (
                        <div className="empty-services">
                            <img src="/assets/icons/no-services.png" alt="No services" className="empty-icon" />
                            <h4>No Services Yet</h4>
                            <p>No service history found for this pet</p>
                        </div>
                    ) : (
                        <div className="services-list">
                            {services.map(service => (
                                <div key={service.id} className="service-item">
                                    <div className="service-main">
                                        <div className="service-type">{service.service_type}</div>
                                        <div className="service-date">{formatDate(service.date)}</div>
                                        {getStatusBadge(service.status)}
                                    </div>
                                    {service.return_date && (
                                        <div className="service-return">
                                            Return: {formatDate(service.return_date)}
                                        </div>
                                    )}
                                    {service.notes && (
                                        <div className="service-notes">
                                            <strong>Notes:</strong> {service.notes}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
          </div>
        </div>
      )}

      {/* Edit Pet Modal */}
      {showEditModal && (
        <div className="modal-overlay" onClick={closeEditModal}>
          <div className="pet-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Edit Pet</h2>
              <button className="close-btn" onClick={closeEditModal}>×</button>
            </div>

            <form onSubmit={handleEditSubmit}>
              <div className="form-section">
                <h3>Basic Information</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label>Pet Name</label>
                    <input
                      type="text"
                      name="petName"
                      value={editForm.petName}
                      onChange={handleEditChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Color</label>
                    <input
                      type="text"
                      name="petColor"
                      value={editForm.petColor}
                      onChange={handleEditChange}
                      required
                    />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Breed</label>
                    <input
                      type="text"
                      name="breed"
                      value={editForm.breed}
                      onChange={handleEditChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Species</label>
                    <select
                      name="species"
                      value={editForm.species}
                      onChange={handleEditChange}
                      required
                    >
                      <option value="" disabled>Select Species</option>
                      <option value="dog">Dog</option>
                      <option value="cat">Cat</option>
                      <option value="others">Others</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="form-section">
                <h3>Other Information</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label>Birthday</label>
                    <input
                      type="date"
                      name="birthDay"
                      value={editForm.birthDay}
                      onChange={handleEditChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Age</label>
                    <input
                      type="text"
                      name="age"
                      value={editForm.age}
                      onChange={handleEditChange}
                      placeholder="Auto-calculated from birthday"
                    />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Sex</label>
                    <select
                      name="sex"
                      value={editForm.sex}
                      onChange={handleEditChange}
                      required
                    >
                      <option value="">Select Sex</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Remarks</label>
                    <input
                      type="text"
                      name="remarks"
                      value={editForm.remarks}
                      onChange={handleEditChange}
                      placeholder="Optional"
                    />
                  </div>
                </div>
              </div>

              <div className="modal-actions">
                <button type="button" className="cancel-btn" onClick={closeEditModal}>
                  CANCEL
                </button>
                <button type="submit" className="save-btn">
                  SAVE CHANGES
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="modal-overlay" onClick={cancelDelete}>
          <div className="confirm-modal" onClick={(e) => e.stopPropagation()}>
            <div className="confirm-header">
              <h3>Confirm Delete</h3>
            </div>
            <div className="confirm-content">
              <p>Are you sure you want to delete <strong>{petToDelete?.petName}</strong>?</p>
              <p className="warning-text">This action cannot be undone.</p>
            </div>
            <div className="confirm-actions">
              <button className="cancel-btn" onClick={cancelDelete}>
                Cancel
              </button>
              <button className="confirm-delete-btn" onClick={confirmDelete}>
                Delete Pet
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}