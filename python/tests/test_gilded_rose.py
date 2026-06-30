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

    def test_expired_item(self):
        # Once the sell by date has passed, Quality degrades twice as fast
        items = [Item("Armor", 0, 8)]
        original_quality = items[0].quality
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(original_quality - 2, items[0].quality)

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

    def test_brie_quality_increases(self):
        # The Quality of Aged Brie goes up, not down
        items = [Item("Aged Brie", 10, 40)]
        original_quality = items[0].quality
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, original_quality + 1)

    def test_sulfuras_never_changes(self):
        # The Quality of Sulfuras never changes
        items = [Item("Sulfuras, Hand of Ragnaros", 10, 80)]
        original_quality = items[0].quality
        original_sell_in = items[0].sell_in
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, original_quality)
        self.assertEqual(items[0].sell_in, original_sell_in)

    def test_backstage_pass_more_than_10_days_increases_quality_by_one(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 10)]
        original_quality = items[0].quality
        original_sell_in = items[0].sell_in
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, original_sell_in - 1)
        self.assertEqual(items[0].quality, original_quality + 1)

    def test_backstage_pass_10_days_or_less_increases_quality_by_two(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 9, 10)]
        original_quality = items[0].quality
        original_sell_in = items[0].sell_in
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, original_sell_in - 1)
        self.assertEqual(items[0].quality, original_quality + 2)

    def test_backstage_pass_5_days_or_less_increases_quality_by_three(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 4, 10)]
        original_quality = items[0].quality
        original_sell_in = items[0].sell_in
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, original_sell_in - 1)
        self.assertEqual(items[0].quality, original_quality + 3)

    def test_backstage_pass_on_concert_day_drops_quality_to_zero(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 10)]
        original_sell_in = items[0].sell_in
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, original_sell_in - 1)
        self.assertEqual(items[0].quality, 0)
 

if __name__ == '__main__':
    unittest.main()
