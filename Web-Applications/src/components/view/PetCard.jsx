const PetCard = ({ pet, onClick }) => {
  // Get species icon based on actual pet data
  const getSpeciesIcon = (species) => {
    const speciesLower = species?.toLowerCase();
    if (speciesLower === 'dog') return 'fas fa-dog';
    if (speciesLower === 'cat') return 'fas fa-cat';
    return 'fas fa-paw'; // default icon
  };

  return (
    <div className="pet-card" onClick={() => onClick(pet)} style={{ cursor: 'pointer' }}>
      <div className="pet-image">
        <i className={getSpeciesIcon(pet.species)}></i>
      </div>
      <div className="pet-info">
        <h4 className="pet-name">{pet.petName}</h4>
        <div className="pet-details">
          <span className="pet-detail">{pet.breed}</span>
          <span className="pet-detail">{pet.sex}</span>
          <span className="pet-detail">{pet.age || 'Unknown'}</span>
        </div>
        <p>{pet.remarks || 'No additional information'}</p>
        <div className="pet-actions petCardActions">
          <button className="btn new-btn-small viewPetDetails" onClick={(e) => { e.stopPropagation(); onClick(pet); }}>
            View Details
          </button>

        </div>
      </div>
    </div>
  )
}

export default PetCard