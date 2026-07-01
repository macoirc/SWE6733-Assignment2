# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_normal_item(self):
        # At the end of the day, our system lowers both values for every item
        items = [Item("Potion", 5, 5)]
        original_quality = items[0].quality
        original_sell_in = items[0].sell_in
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(original_quality - 1, items[0].quality)
        self.assertEqual(original_sell_in - 1, items[0].sell_in)

    def test_quality_not_negative(self):
        # The Quality of an item is never negative
        items = [Item("Chain Mail", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertGreaterEqual(items[0].quality, 0)

    def test_quality_50_or_less(self):
        # The Quality of an item is never more than 50
        items = [Item("Aged Brie", 0, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertLessEqual(items[0].quality, 50)

    def test_expired_item(self):
        # Once the sell by date has passed, Quality degrades twice as fast
        items = [
            Item("Armor", 0, 8), 
            Item("Map", -1, 10)
            ]
        for item in items:
            original_quality = item.quality
            gilded_rose = GildedRose([item])
            gilded_rose.update_quality()
            self.assertEqual(original_quality - 2, item.quality)

    def test_brie_quality_increases(self):
        # The Quality of Aged Brie goes up, not down, and twice as fast after the sell by date has passed
        items = [
            Item("Aged Brie", 10, 10),
            Item("Aged Brie", 0, 20),
            Item("Aged Brie", -5, 25)
        ]
        for item in items:
            original_quality = item.quality
            gilded_rose = GildedRose([item])
            gilded_rose.update_quality()
            if item.sell_in < 0:
                self.assertEqual(item.quality, original_quality + 2)
            else:
                self.assertEqual(item.quality, original_quality + 1)

    def test_sulfuras_never_changes(self):
        # The Quality of Sulfuras never changes
        items = [
            Item("Sulfuras, Hand of Ragnaros", 10, 80),
            Item("Sulfuras, Hand of Ragnaros", 0, 80),
            Item("Sulfuras, Hand of Ragnaros", -5, 80)
            ]
        for item in items:
            original_quality = item.quality
            original_sell_in = item.sell_in
            gilded_rose = GildedRose([item])
            gilded_rose.update_quality()
            self.assertEqual(item.quality, original_quality)
            self.assertEqual(item.sell_in, original_sell_in)

    def test_backstage_passes(self):
        # The Quality of Backstage passes increases by 2 when there are 10 days or less and by 3 when there are 5 days or less 
        # but Quality drops to 0 after the concert
        items = [
            Item("Backstage passes to a TAFKAL80ETC concert", 15, 10),
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 20),
            Item("Backstage passes to a TAFKAL80ETC concert", 5, 30),
            Item("Backstage passes to a TAFKAL80ETC concert", 0, 40),
            Item("Backstage passes to a TAFKAL80ETC concert", -1, 0)
        ]
        for item in items:
            original_quality = item.quality
            gilded_rose = GildedRose([item])
            gilded_rose.update_quality()
            if item.sell_in > 10:
                self.assertEqual(item.quality, original_quality + 1)
            elif item.sell_in > 5:
                self.assertEqual(item.quality, original_quality + 2)
            elif item.sell_in > 0:
                self.assertEqual(item.quality, original_quality + 3)
            else:
                self.assertEqual(item.quality, 0)

if __name__ == '__main__':
    unittest.main()
