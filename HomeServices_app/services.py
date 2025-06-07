class AIServices:
    """Service class for AI-powered recommendations"""
    
    def __init__(self):
        self.service_categories = [
            'Plumbing',
            'Electrical',
            'Carpentry',
            'Cleaning',
            'Painting',
            'Gardening',
            'Appliance Repair',
            'HVAC',
            'Pest Control',
            'Moving'
        ]

    def get_service_recommendation(self, description):
        """
        Analyze user description and recommend appropriate services
        Args:
            description (str): User's description of their needs
        Returns:
            dict: Recommendation result
        """
        try:
            # Simple keyword matching for now
            # In a real implementation, this would use more sophisticated NLP
            description = description.lower()
            matches = []
            
            keywords = {
                'Plumbing': ['water', 'pipe', 'leak', 'tap', 'drain', 'toilet', 'sink'],
                'Electrical': ['power', 'electric', 'light', 'switch', 'wire', 'outlet'],
                'Carpentry': ['wood', 'door', 'cabinet', 'furniture', 'shelf'],
                'Cleaning': ['clean', 'dust', 'wash', 'mop', 'vacuum'],
                'Painting': ['paint', 'wall', 'color', 'stain'],
                'Gardening': ['plant', 'garden', 'lawn', 'tree', 'grass'],
                'Appliance Repair': ['refrigerator', 'washer', 'dryer', 'dishwasher', 'appliance'],
                'HVAC': ['air', 'heating', 'cooling', 'ac', 'ventilation'],
                'Pest Control': ['pest', 'bug', 'insect', 'rat', 'termite'],
                'Moving': ['move', 'relocate', 'transport', 'shift']
            }
            
            for service, words in keywords.items():
                if any(word in description for word in words):
                    matches.append(service)
            
            if matches:
                return {
                    'error': False,
                    'recommendations': matches,
                    'message': 'Based on your description, we recommend these services'
                }
            else:
                return {
                    'error': False,
                    'recommendations': [],
                    'message': 'Please provide more specific details about the service you need'
                }
                
        except Exception as e:
            return {
                'error': True,
                'message': f'Error processing recommendation: {str(e)}'
            } 