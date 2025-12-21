"""
Tests for visualizer
"""

import pytest
from src.genetics import GeneticsEngine
from src.visualizer import MonkeyVisualizer


class TestMonkeyVisualizer:
    """Test monkey visualizer"""
    
    def test_generate_svg(self):
        """Test SVG generation"""
        dna = GeneticsEngine.generate_random_dna()
        svg = MonkeyVisualizer.generate_svg(dna)
        
        assert isinstance(svg, str)
        assert svg.startswith('<svg')
        assert svg.endswith('</svg>')
        assert 'width="400"' in svg
        assert 'height="400"' in svg
    
    def test_svg_contains_elements(self):
        """Test SVG contains expected elements"""
        dna = GeneticsEngine.generate_random_dna()
        svg = MonkeyVisualizer.generate_svg(dna)
        
        # Should contain basic elements
        assert '<ellipse' in svg or '<circle' in svg  # Head/body
        assert '<defs>' in svg  # Definitions
        assert '<rect' in svg or '<path' in svg  # Background or paths
    
    def test_thumbnail_generation(self):
        """Test thumbnail generation"""
        dna = GeneticsEngine.generate_random_dna()
        thumbnail = MonkeyVisualizer.generate_thumbnail(dna, size=100)
        
        assert isinstance(thumbnail, str)
        assert 'width="100"' in thumbnail
        assert 'height="100"' in thumbnail
    
    def test_different_dna_different_svg(self):
        """Test different DNA produces different SVG"""
        dna1 = GeneticsEngine.generate_random_dna()
        dna2 = GeneticsEngine.generate_random_dna()
        
        svg1 = MonkeyVisualizer.generate_svg(dna1)
        svg2 = MonkeyVisualizer.generate_svg(dna2)
        
        # Very unlikely to be identical
        assert svg1 != svg2
    
    def test_color_mapping(self):
        """Test color mapping exists"""
        assert hasattr(MonkeyVisualizer, 'BODY_COLORS') or hasattr(MonkeyVisualizer, 'COLORS')
        colors = getattr(MonkeyVisualizer, 'BODY_COLORS', getattr(MonkeyVisualizer, 'COLORS', {}))
        assert "brown" in colors or len(colors) > 0
    
    def test_svg_valid_structure(self):
        """Test SVG has valid structure"""
        dna = GeneticsEngine.generate_random_dna()
        svg = MonkeyVisualizer.generate_svg(dna)
        
        # Count opening and closing tags
        assert svg.count('<svg') == svg.count('</svg>')
        assert svg.count('<defs>') == svg.count('</defs>')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
