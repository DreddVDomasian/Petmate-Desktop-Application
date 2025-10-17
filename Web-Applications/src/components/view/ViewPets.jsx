import React, { useState, useEffect } from 'react';
import { getCookie } from '../../utils/csrf';

export default function ViewPets() {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPet, setSelectedPet] = useState(null);
  const [showPetModal, setShowPetModal] = useState(false);

  useEffect(() => {
    fetchUserPets();
  }, []);

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
      } else {
        console.error('Failed to fetch pets');
      }
    } catch (error) {
      console.error('Error fetching pets:', error);
    } finally {
      setLoading(false);
    }
  };

  const openPetModal = (pet) => {
    setSelectedPet(pet);
    setShowPetModal(true);
  };

  const closePetModal = () => {
    setSelectedPet(null);
    setShowPetModal(false);
  };

  const getSpeciesIcon = (species) => {
    const speciesLower = species?.toLowerCase();
    if (speciesLower === 'dog') return '../../../public/assets/icons/dog.png';
    if (speciesLower === 'cat') return '../../../public/assets/icons/catIcon.png';
    return '/assets/icons/other-pet.png';
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

      {/* Pet Detail Modal */}
      {showPetModal && selectedPet && (
        <div className="modal-overlay" onClick={closePetModal}>
          <div className="pet-modal" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                  <h2>Pet Details</h2>
                  <button className="close-btn" onClick={closePetModal}>×</button>
              </div>


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
                <button className="DeletePetBtn">
                  DELETE PET
                </button>
                <button className="EditPetBtn">
                  EDIT PET
                </button>
              </div>
          </div>
        </div>
      )}
    </div>
  );
}