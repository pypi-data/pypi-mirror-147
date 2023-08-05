/*
 * VegaFusion
 * Copyright (C) 2022 VegaFusion Technologies LLC
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License along with this program.
 * If not, see http://www.gnu.org/licenses/.
 */
pub mod aggregate;
pub mod bin;
pub mod collect;
pub mod extent;
pub mod filter;
pub mod formula;
pub mod joinaggregate;
pub mod lookup;
pub mod sequence;
pub mod timeunit;
pub mod unsupported;
pub mod window;

use crate::spec::transform::{extent::ExtentTransformSpec, filter::FilterTransformSpec};

use crate::error::Result;
use crate::spec::transform::aggregate::AggregateTransformSpec;
use crate::spec::transform::bin::BinTransformSpec;
use crate::spec::transform::collect::CollectTransformSpec;
use crate::spec::transform::formula::FormulaTransformSpec;
use crate::spec::transform::joinaggregate::JoinAggregateTransformSpec;
use crate::spec::transform::lookup::LookupTransformSpec;
use crate::spec::transform::sequence::SequenceTransformSpec;
use crate::spec::transform::timeunit::TimeUnitTransformSpec;
use crate::spec::transform::unsupported::*;
use crate::spec::transform::window::WindowTransformSpec;
use crate::task_graph::task::InputVariable;
use serde::{Deserialize, Serialize};
use std::ops::Deref;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "lowercase")]
pub enum TransformSpec {
    Extent(ExtentTransformSpec),
    Filter(FilterTransformSpec),
    Formula(FormulaTransformSpec),
    Bin(Box<BinTransformSpec>), // Box since transform is much larger than others
    Aggregate(AggregateTransformSpec),
    Collect(CollectTransformSpec),
    Timeunit(TimeUnitTransformSpec),
    JoinAggregate(JoinAggregateTransformSpec),
    Window(WindowTransformSpec),

    // Unsupported
    CountPattern(CountpatternTransformSpec),
    Contour(ContourTransformSpec),
    Cross(CrossTransformSpec),
    Crossfilter(CrossfilterTransformSpec),
    Density(DensityTransformSpec),
    DotBin(DotbinTransformSpec),
    Flatten(FlattenTransformSpec),
    Fold(FoldTransformSpec),
    Force(ForceTransformSpec),
    GeoJson(GeojsonTransformSpec),
    GeoPath(GeopathTransformSpec),
    GeoPoint(GeopointTransformSpec),
    GeoShape(GeoshapeTransformSpec),
    Graticule(GraticuleTransformSpec),
    Heatmap(HeatmapTransformSpec),
    Identifier(IdentifierTransformSpec),
    Impute(ImputeTransformSpec),
    IsoContour(IsocontourTransformSpec),
    Kde(KdeTransformSpec),
    Kde2d(Kde2dTransformSpec),
    Label(LabelTransformSpec),
    LinkPath(LinkpathTransformSpec),
    Loess(LoessTransformSpec),
    Lookup(LookupTransformSpec),
    Nest(NestTransformSpec),
    Pack(PackTransformSpec),
    Partition(PartitionTransformSpec),
    Pie(PieTransformSpec),
    Pivot(PivotTransformSpec),
    Project(ProjectTransformSpec),
    Quantile(QuantileTransformSpec),
    Regression(RegressionTransformSpec),
    ResolveFilter(ResolvefilterTransformSpec),
    Sample(SampleTransformSpec),
    Sequence(SequenceTransformSpec),
    Stack(StackTransformSpec),
    Stratify(StratifyTransformSpec),
    Tree(TreeTransformSpec),
    TreeLinks(TreelinksTransformSpec),
    Treemap(TreemapTransformSpec),
    Voronoi(VoronoiTransformSpec),
    WordCloud(WordcloudTransformSpec),
}

impl Deref for TransformSpec {
    type Target = dyn TransformSpecTrait;

    fn deref(&self) -> &Self::Target {
        match self {
            TransformSpec::Extent(t) => t,
            TransformSpec::Filter(t) => t,
            TransformSpec::Formula(t) => t,
            TransformSpec::Bin(t) => t.as_ref(),
            TransformSpec::Aggregate(t) => t,
            TransformSpec::Collect(t) => t,
            TransformSpec::Timeunit(t) => t,

            // Supported for dependency determination, not implementation
            TransformSpec::Lookup(t) => t,
            TransformSpec::Sequence(t) => t,

            // Unsupported
            TransformSpec::CountPattern(t) => t,
            TransformSpec::Contour(t) => t,
            TransformSpec::Cross(t) => t,
            TransformSpec::Crossfilter(t) => t,
            TransformSpec::Density(t) => t,
            TransformSpec::DotBin(t) => t,
            TransformSpec::Flatten(t) => t,
            TransformSpec::Fold(t) => t,
            TransformSpec::Force(t) => t,
            TransformSpec::GeoJson(t) => t,
            TransformSpec::GeoPath(t) => t,
            TransformSpec::GeoPoint(t) => t,
            TransformSpec::GeoShape(t) => t,
            TransformSpec::Graticule(t) => t,
            TransformSpec::Heatmap(t) => t,
            TransformSpec::Identifier(t) => t,
            TransformSpec::Impute(t) => t,
            TransformSpec::IsoContour(t) => t,
            TransformSpec::JoinAggregate(t) => t,
            TransformSpec::Kde(t) => t,
            TransformSpec::Kde2d(t) => t,
            TransformSpec::Label(t) => t,
            TransformSpec::LinkPath(t) => t,
            TransformSpec::Loess(t) => t,
            TransformSpec::Nest(t) => t,
            TransformSpec::Pack(t) => t,
            TransformSpec::Partition(t) => t,
            TransformSpec::Pie(t) => t,
            TransformSpec::Pivot(t) => t,
            TransformSpec::Project(t) => t,
            TransformSpec::Quantile(t) => t,
            TransformSpec::Regression(t) => t,
            TransformSpec::ResolveFilter(t) => t,
            TransformSpec::Sample(t) => t,
            TransformSpec::Stack(t) => t,
            TransformSpec::Stratify(t) => t,
            TransformSpec::Tree(t) => t,
            TransformSpec::TreeLinks(t) => t,
            TransformSpec::Treemap(t) => t,
            TransformSpec::Voronoi(t) => t,
            TransformSpec::Window(t) => t,
            TransformSpec::WordCloud(t) => t,
        }
    }
}

pub trait TransformSpecTrait {
    fn supported(&self) -> bool {
        true
    }

    fn output_signals(&self) -> Vec<String> {
        Default::default()
    }

    fn input_vars(&self) -> Result<Vec<InputVariable>> {
        Ok(Default::default())
    }
}
