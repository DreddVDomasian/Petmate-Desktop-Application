import React, { useState, useEffect } from 'react';
import { getCookie } from '../../utils/csrf';

const PetDetailsModal = ({ isOpen, onClose, pet, onPetUpdated, onPetDeleted }) => {
  const [services, setServices] = useState([]);
  const [servicesLoading, setServicesLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('details');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editForm, setEditForm] = useState({
    petName: '',
    petColor: '',
    breed: '',
    species: '',
    customSpecies: '',
    birthDay: '',
    age: '',
    sex: '',
    remarks: ''
  });

  useEffect(() => {
    if (pet && isOpen) {
      fetchPetServices(pet.id);
    }
  }, [pet, isOpen]);

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

  const handleTabClick = (tab) => {
    setActiveTab(tab);
    if (tab === 'services' && pet && services.length === 0) {
      fetchPetServices(pet.id);
    }
  };

  const openEditModal = () => {
    if (!pet) return;

    const speciesLower = pet.species?.toLowerCase() || "";
    let species = speciesLower;
    let customSpecies = "";

    if (speciesLower !== "dog" && speciesLower !== "cat") {
      species = "others";
      customSpecies = pet.species;
    }

    setEditForm({
      petName: pet.petName || '',
      petColor: pet.petColor || '',
      breed: pet.breed || '',
      species: species,
      customSpecies: customSpecies,
      birthDay: pet.birthDay || '',
      age: pet.age || '',
      sex: pet.sex || '',
      remarks: pet.remarks || ''
    });

    setShowEditModal(true);
  };

  const closeEditModal = () => {
    setShowEditModal(false);
    setEditForm({
      petName: '',
      petColor: '',
      breed: '',
      species: '',
      customSpecies: '',
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

      if (name === 'birthDay' && value) {
        updatedForm.age = calculateAge(value);
      }

      return updatedForm;
    });
  };

  const handleAgeChange = (e) => {
    const { value } = e.target;
    setEditForm(prev => ({
      ...prev,
      age: value,
      birthDay: value ? '' : prev.birthDay
    }));
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    if (!pet) return;

    let finalSpecies = editForm.species;
    if (finalSpecies === "others") {
      if (!editForm.customSpecies.trim()) {
        alert("Please specify the species name");
        return;
      }
      finalSpecies = editForm.customSpecies.trim();
    }

    try {
      const res = await fetch(`/api/pets/${pet.id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        credentials: 'include',
        body: JSON.stringify({
          petName: editForm.petName,
          petColor: editForm.petColor,
          breed: editForm.breed,
          species: finalSpecies,
          birthDate: editForm.birthDay || null,
          stored_age: editForm.birthDay ? null : (editForm.age || null),
          sex: editForm.sex,
          remarks: editForm.remarks?.trim() || null
        })
      });

      if (res.ok) {
        alert('Pet updated successfully!');
        closeEditModal();
        onClose();
        if (onPetUpdated) onPetUpdated();
      } else {
        throw new Error('Failed to update pet');
      }
    } catch (error) {
      console.error('Error updating pet:', error);
      alert('Error updating pet. Please try again.');
    }
  };

  const handleDeleteClick = () => {
    setShowDeleteConfirm(true);
  };

  const confirmDelete = async () => {
    if (!pet) return;

    try {
      const res = await fetch(`/api/pets/${pet.id}/`, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        credentials: 'include'
      });

      if (res.ok) {
        alert('Pet deleted successfully!');
        setShowDeleteConfirm(false);
        onClose();
        if (onPetDeleted) onPetDeleted();
      } else {
        throw new Error('Failed to delete pet');
      }
    } catch (error) {
      console.error('Error deleting pet:', error);
      alert('Error deleting pet. Please try again.');
    }
  };

  const cancelDelete = () => {
    setShowDeleteConfirm(false);
  };

  const getSpeciesIcon = (species) => {
    const speciesLower = species?.toLowerCase();
    if (speciesLower === 'dog') return 'fas fa-dog';
    if (speciesLower === 'cat') return 'fas fa-cat';
    return 'fas fa-paw';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not specified';
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

  if (!isOpen || !pet) return null;

  return (
    <>
      {/* Main Pet Details Modal */}
      <div className="modal active" onClick={onClose}>
        <div className="new-modal-content" onClick={(e) => e.stopPropagation()}>
          <div className="new-modal-header">
            <h3 className="modal-title">Pet Details - {pet.petName}</h3>
            <button className="modal-close" onClick={onClose}>&times;</button>
          </div>
          <div className="modal-body">
            <div className="modal-tabs" style={{ marginBottom: '10x' }}>
              <button
                className={`tab ${activeTab === 'details' ? 'active' : ''}`}
                onClick={() => handleTabClick('details')}
                style={{ 
                  padding: '10px 20px', 
                  border: 'none', 
                  background: 'none',
                  borderBottom: activeTab === 'details' ? '3px solid var(--secondary)' : '3px solid transparent',
                  color: activeTab === 'details' ? 'var(--primary)' : 'var(--dark)',
                  cursor: 'pointer',
                  fontWeight: '600'
                }}
              >
                Details
              </button>
              <button
                className={`tab ${activeTab === 'services' ? 'active' : ''}`}
                onClick={() => handleTabClick('services')}
                style={{ 
                  padding: '10px 20px', 
                  border: 'none', 
                  background: 'none',
                  borderBottom: activeTab === 'services' ? '3px solid var(--secondary)' : '3px solid transparent',
                  color: activeTab === 'services' ? 'var(--primary)' : 'var(--dark)',
                  cursor: 'pointer',
                  fontWeight: '600'
                }}
              >
                Service History
              </button>
            </div>

            {activeTab === 'details' && (
              <div className="details-container">
                <div className="pet-profile-header" style={{ display: 'flex', alignItems: 'center', marginBottom: '30px', padding: '20px', background: 'var(--gray)', borderRadius: '8px' }}>
                  <div className="profile-pet-icon" style={{ fontSize: '3rem', color: 'var(--primary)', marginRight: '20px' }}>
                    <i className={getSpeciesIcon(pet.species)}></i>
                  </div>
                  <div className="pet-profile-info">
                    <h1 style={{ margin: '0 0 5px 0', color: 'var(--primary)' }}>{pet.petName}</h1>
                    <p className="pet-breed" style={{ margin: 0, color: 'var(--dark)' }}>{pet.breed}</p>
                  </div>
                </div>

                <div className="details-grid">
                  <div className="detail-section" style={{ marginBottom: '25px' }}>
                    <h3 style={{ color: 'var(--primary)', marginBottom: '15px' }}>Basic Information</h3>
                    <div className="detail-row" style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #eee' }}>
                      <span className="detail-label" style={{ fontWeight: '600', color: 'var(--accent)' }}>Species:</span>
                      <span className="detail-value">{pet.species}</span>
                    </div>
                    <div className="detail-row" style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #eee' }}>
                      <span className="detail-label" style={{ fontWeight: '600', color: 'var(--accent)' }}>Color:</span>
                      <span className="detail-value">{pet.petColor}</span>
                    </div>
                    <div className="detail-row" style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #eee' }}>
                      <span className="detail-label" style={{ fontWeight: '600', color: 'var(--accent)' }}>Sex:</span>
                      <span className="detail-value">{pet.sex}</span>
                    </div>
                  </div>

                  <div className="detail-section" style={{ marginBottom: '25px' }}>
                    <h3 style={{ color: 'var(--primary)', marginBottom: '15px' }}>Age Information</h3>
                    <div className="detail-row" style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #eee' }}>
                      <span className="detail-label" style={{ fontWeight: '600', color: 'var(--accent)' }}>Birthday:</span>
                      <span className="detail-value">
                        {pet.birthDay ? formatDate(pet.birthDay) : 'Not specified'}
                      </span>
                    </div>
                    <div className="detail-row" style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #eee' }}>
                      <span className="detail-label" style={{ fontWeight: '600', color: 'var(--accent)' }}>Age:</span>
                      <span className="detail-value">{pet.age || 'Unknown'}</span>
                    </div>
                  </div>

                  {pet.remarks && (
                    <div className="detail-section" style={{ marginBottom: '25px' }}>
                      <h3 style={{ color: 'var(--primary)', marginBottom: '15px' }}>Remarks</h3>
                      <p className="remarks-text" style={{ padding: '15px', background: 'var(--gray)', borderRadius: '8px', margin: 0 }}>
                        {pet.remarks}
                      </p>
                    </div>
                  )}
                </div>

                <div className="modal-actions">
                  <button
                    className="btn"
                    onClick={handleDeleteClick}
                    style={{ background: '#ff6b6b', color: 'white' }}
                  >
                    DELETE PET
                  </button>
                  <button
                    className="btn new-btn-primary"
                    onClick={openEditModal}
                  >
                    EDIT PET
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'services' && (
              <div className="services-container">
                <div className="services-header" style={{ marginBottom: '25px' }}>
                  <h3 style={{ color: 'var(--primary)', marginBottom: '10px' }}>Service History for {pet.petName}</h3>
                  <p style={{ color: 'var(--dark)' }}>All medical services and appointments</p>
                </div>

                {servicesLoading ? (
                  <div className="loading" style={{ textAlign: 'center', padding: '40px' }}>Loading services...</div>
                ) : services.length === 0 ? (
                  <div className="empty-services" style={{ textAlign: 'center', padding: '40px', color: 'var(--dark)' }}>
                    <i className="fas fa-clipboard-list" style={{ fontSize: '3rem', color: 'var(--primary)', marginBottom: '15px', opacity: '0.5' }}></i>
                    <h4>No Services Yet</h4>
                    <p>No service history found for this pet</p>
                  </div>
                ) : (
                  <div className="services-list">
                    {services.map(service => (
                      <div key={service.id} className="service-item" style={{ 
                        padding: '20px', 
                        border: '1px solid #eee', 
                        borderRadius: '8px', 
                        marginBottom: '15px',
                        background: 'white'
                      }}>
                        <div className="service-main" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                          <div className="service-type" style={{ fontWeight: '600', color: 'var(--primary)' }}>{service.service_type}</div>
                          <div className="service-date" style={{ color: 'var(--dark)' }}>{formatDate(service.date)}</div>
                          {getStatusBadge(service.status)}
                        </div>
                        {service.return_date && (
                          <div className="service-return" style={{ color: 'var(--accent)', marginBottom: '5px' }}>
                            <strong>Return:</strong> {formatDate(service.return_date)}
                          </div>
                        )}
                        {service.notes && (
                          <div className="service-notes" style={{ color: 'var(--dark)' }}>
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
      </div>

      {/* Edit Pet Modal */}
      {showEditModal && (
        <div className="modal active" onClick={closeEditModal}>
          <div className="new-modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="new-modal-header">
              <h3 className="modal-title">Edit Pet - {pet.petName}</h3>
              <button className="modal-close" onClick={closeEditModal}>&times;</button>
            </div>
            <div className="modal-body">
              <form onSubmit={handleEditSubmit}>
                <div className="new-form-group">
                  <label>Pet Name</label>
                  <input
                    type="text"
                    name="petName"
                    className="form-control"
                    value={editForm.petName}
                    onChange={handleEditChange}
                    required
                  />
                </div>
                
                <div className="new-form-row" style={{ display: 'flex', gap: '15px' }}>
                  <div className="new-form-group" style={{ flex: 1 }}>
                    <label>Color</label>
                    <input
                      type="text"
                      name="petColor"
                      className="form-control"
                      value={editForm.petColor}
                      onChange={handleEditChange}
                      required
                    />
                  </div>
                  <div className="new-form-group" style={{ flex: 1 }}>
                    <label>Breed</label>
                    <input
                      type="text"
                      name="breed"
                      className="form-control"
                      value={editForm.breed}
                      onChange={handleEditChange}
                      required
                    />
                  </div>
                </div>

                <div className="new-form-row" style={{ display: 'flex', gap: '15px' }}>
                  <div className="new-form-group" style={{ flex: 1 }}>
                    <label>Species</label>
                    <select
                      name="species"
                      className="form-control"
                      value={editForm.species}
                      onChange={handleEditChange}
                      required
                    >
                      <option value="">Select Species</option>
                      <option value="dog">Dog</option>
                      <option value="cat">Cat</option>
                      <option value="others">Others</option>
                    </select>
                  </div>
                </div>

                {editForm.species === "others" && (
                  <div className="new-form-group">
                    <label>Specify Species</label>
                    <input
                      type="text"
                      name="customSpecies"
                      className="form-control"
                      placeholder="Type specific species (e.g., Hamster)"
                      value={editForm.customSpecies}
                      onChange={handleEditChange}
                      required
                    />
                  </div>
                )}
                
                <div className="new-form-row" style={{ display: 'flex', gap: '15px' }}>
                  <div className="new-form-group" style={{ flex: 1 }}>
                    <label>Birthday</label>
                    <input
                      type="date"
                      name="birthDay"
                      className="form-control"
                      value={editForm.birthDay}
                      onChange={handleEditChange}
                      max={new Date().toLocaleDateString('en-CA')}
                    />
                  </div>
                  <div className="new-form-group" style={{ flex: 1 }}>
                    <label>Age</label>
                    <input
                      type="text"
                      name="age"
                      className="form-control"
                      value={editForm.age}
                      onChange={handleAgeChange}
                      placeholder="Auto-calculated from birthday"
                    />
                  </div>
                </div>
                
                <div className="new-form-row" style={{ display: 'flex', gap: '15px' }}>
                  <div className="new-form-group" style={{ flex: 1 }}>
                    <label>Sex</label>
                    <select
                      name="sex"
                      className="form-control"
                      value={editForm.sex}
                      onChange={handleEditChange}
                      required
                    >
                      <option value="">Select Sex</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                    </select>
                  </div>
                </div>
                
                <div className="new-form-group">
                  <label>Remarks</label>
                  <textarea
                    name="remarks"
                    className="form-control"
                    placeholder="Any additional information about your pet"
                    rows="3"
                    value={editForm.remarks}
                    onChange={handleEditChange}
                  ></textarea>
                </div>
                
                <div className="new-form-group" style={{ display: 'flex', gap: '15px', justifyContent: 'flex-end' }}>
                  <button type="button" className="btn" onClick={closeEditModal}>Cancel</button>
                  <button type="submit" className="btn new-btn-primary">Save Changes</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="modal active" onClick={cancelDelete}>
          <div className="new-modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="new-modal-header">
              <h3 className="modal-title">Confirm Delete</h3>
              <button className="modal-close" onClick={cancelDelete}>&times;</button>
            </div>
            <div className="modal-body">
              <div style={{ textAlign: 'center', padding: '20px' }}>
                <p>Are you sure you want to delete <strong>{pet.petName}</strong>?</p>
                <p style={{ color: '#ff6b6b', fontWeight: '600' }}>This action cannot be undone.</p>
              </div>
              <div style={{ display: 'flex', gap: '15px', justifyContent: 'flex-end' }}>
                <button className="btn" onClick={cancelDelete}>Cancel</button>
                <button className="btn" onClick={confirmDelete} style={{ background: '#ff6b6b', color: 'white' }}>
                  Delete Pet
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default PetDetailsModal;